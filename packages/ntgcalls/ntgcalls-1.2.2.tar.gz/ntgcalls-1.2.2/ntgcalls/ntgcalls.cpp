//
// Created by Laky64 on 22/08/2023.
//

#include "ntgcalls.hpp"

#include <iostream>

#include "exceptions.hpp"
#include "instances/group_call.hpp"
#include "instances/p2p_call.hpp"
#include "models/dh_config.hpp"

namespace ntgcalls {
    NTgCalls::NTgCalls() {
        updateThread = rtc::Thread::Create();
        updateThread->Start();
        hardwareInfo = std::make_unique<HardwareInfo>();
        INIT_ASYNC
        LogSink::GetOrCreate();
    }

    NTgCalls::~NTgCalls() {
#ifdef PYTHON_ENABLED
        py::gil_scoped_release release;
#endif
        std::unique_lock lock(mutex);
        RTC_LOG(LS_VERBOSE) << "Destroying NTgCalls";
        connections = {};
        hardwareInfo = nullptr;
        lock.unlock();
        updateThread->Stop();
        updateThread = nullptr;
        DESTROY_ASYNC
        RTC_LOG(LS_VERBOSE) << "NTgCalls destroyed";
        LogSink::UnRef();
    }

    void NTgCalls::setupListeners(const int64_t chatId) {
        connections[chatId]->onStreamEnd([this, chatId](const Stream::Type &type) {
            WORKER("onStreamEnd", updateThread, this, chatId, type)
            THREAD_SAFE
            (void) onEof(chatId, type);
            END_THREAD_SAFE
            END_WORKER
        });
        if (connections[chatId]->type() & CallInterface::Type::Group) {
            SafeCall<GroupCall>(connections[chatId].get())->onUpgrade([this, chatId](const MediaState &state) {
                WORKER("onUpgrade", updateThread, this, chatId, state)
                THREAD_SAFE
                (void) mediaStateCallback(chatId, state);
                END_THREAD_SAFE
                END_WORKER
            });
        }
        connections[chatId]->onConnectionChange([this, chatId](const CallInterface::ConnectionState &state) {
            WORKER("onConnectionChange", updateThread, this, chatId, state)
            THREAD_SAFE
            switch (state) {
                case CallInterface::ConnectionState::Closed:
                case CallInterface::ConnectionState::Failed:
                case CallInterface::ConnectionState::Timeout:
                    remove(chatId);
                    break;
                default:
                    break;
            }
            (void) connectionChangeCallback(chatId, state);
            END_THREAD_SAFE
            END_WORKER
        });
        if (connections[chatId]->type() & CallInterface::Type::P2P) {
            SafeCall<P2PCall>(connections[chatId].get())->onSignalingData([this, chatId](const bytes::binary& data) {
                WORKER("onSignalingData", updateThread, this, chatId, data)
                THREAD_SAFE
                (void) emitCallback(chatId, CAST_BYTES(data));
                END_THREAD_SAFE
                END_WORKER
            });
        }
    }

    ASYNC_RETURN(bytes::vector) NTgCalls::createP2PCall(const int64_t userId, const DhConfig& dhConfig, const std::optional<BYTES(bytes::vector)> &g_a_hash, const MediaDescription& media) {
        SMART_ASYNC(this, userId, dhConfig, g_a_hash = CPP_BYTES(g_a_hash, bytes::vector), media)
        std::lock_guard lock(mutex);
        CHECK_AND_THROW_IF_EXISTS(userId)
        connections[userId] = std::make_shared<P2PCall>(updateThread.get());
        setupListeners(userId);
        const auto result = SafeCall<P2PCall>(connections[userId].get())->init(dhConfig, g_a_hash, media);
        THREAD_SAFE
        return CAST_BYTES(result);
        END_THREAD_SAFE
        END_ASYNC
    }

    ASYNC_RETURN(AuthParams) NTgCalls::exchangeKeys(const int64_t userId, const BYTES(bytes::vector) &g_a_or_b, const int64_t fingerprint) {
        SMART_ASYNC(this, userId, g_a_or_b = CPP_BYTES(g_a_or_b, bytes::vector), fingerprint)
        return SafeCall<P2PCall>(safeConnection(userId))->exchangeKeys(g_a_or_b, fingerprint);
        END_ASYNC
    }

    ASYNC_RETURN(void) NTgCalls::connectP2P(const int64_t userId, const std::vector<RTCServer>& servers, const std::vector<std::string>& versions, const bool p2pAllowed) {
        SMART_ASYNC(this, userId, servers, versions, p2pAllowed)
        SafeCall<P2PCall>(safeConnection(userId))->connect(servers, versions, p2pAllowed);
        END_ASYNC
    }

    ASYNC_RETURN(std::string) NTgCalls::createCall(const int64_t chatId, const MediaDescription& media) {
        SMART_ASYNC(this, chatId, media)
        std::lock_guard lock(mutex);
        CHECK_AND_THROW_IF_EXISTS(chatId)
        connections[chatId] = std::make_shared<GroupCall>(updateThread.get());
        setupListeners(chatId);
        return SafeCall<GroupCall>(connections[chatId].get())->init(media);
        END_ASYNC
    }

    ASYNC_RETURN(void) NTgCalls::connect(const int64_t chatId, const std::string& params) {
        SMART_ASYNC(this, chatId, params)
        SafeCall<GroupCall>(safeConnection(chatId))->connect(params);
        END_ASYNC
    }

    ASYNC_RETURN(void) NTgCalls::changeStream(const int64_t chatId, const MediaDescription& media) {
        SMART_ASYNC(this, chatId, media)
        safeConnection(chatId)->changeStream(media);
        END_ASYNC
    }

    ASYNC_RETURN(bool) NTgCalls::pause(const int64_t chatId) {
        SMART_ASYNC(this, chatId)
        return safeConnection(chatId)->pause();
        END_ASYNC
    }

    ASYNC_RETURN(bool) NTgCalls::resume(const int64_t chatId) {
        SMART_ASYNC(this, chatId)
        return safeConnection(chatId)->resume();
        END_ASYNC
    }

    ASYNC_RETURN(bool) NTgCalls::mute(const int64_t chatId) {
        SMART_ASYNC(this, chatId)
        return safeConnection(chatId)->mute();
        END_ASYNC
    }

    ASYNC_RETURN(bool) NTgCalls::unmute(const int64_t chatId) {
        SMART_ASYNC(this, chatId)
        return safeConnection(chatId)->unmute();
        END_ASYNC
    }

    ASYNC_RETURN(void) NTgCalls::stop(const int64_t chatId) {
        SMART_ASYNC(this, chatId)
        remove(chatId);
        END_ASYNC
    }

    void NTgCalls::onStreamEnd(const std::function<void(int64_t, Stream::Type)>& callback) {
        std::lock_guard lock(mutex);
        onEof = callback;
    }

    void NTgCalls::onUpgrade(const std::function<void(int64_t, MediaState)>& callback) {
        std::lock_guard lock(mutex);
        mediaStateCallback = callback;
    }

    void NTgCalls::onConnectionChange(const std::function<void(int64_t, CallInterface::ConnectionState)>& callback) {
       std::lock_guard lock(mutex);
       connectionChangeCallback = callback;
    }

    void NTgCalls::onSignalingData(const std::function<void(int64_t, const BYTES(bytes::binary)&)>& callback) {
        std::lock_guard lock(mutex);
        emitCallback = callback;
    }

    ASYNC_RETURN(void) NTgCalls::sendSignalingData(const int64_t chatId, const BYTES(bytes::binary) &msgKey) {
        SMART_ASYNC(this, chatId, msgKey = CPP_BYTES(msgKey, bytes::binary))
        SafeCall<P2PCall>(safeConnection(chatId))->sendSignalingData(msgKey);
        END_ASYNC
    }

    ASYNC_RETURN(uint64_t) NTgCalls::time(const int64_t chatId) {
        SMART_ASYNC(this, chatId)
        return safeConnection(chatId)->time();
        END_ASYNC
    }

    ASYNC_RETURN(MediaState) NTgCalls::getState(const int64_t chatId) {
        SMART_ASYNC(this, chatId)
        return safeConnection(chatId)->getState();
        END_ASYNC
    }

    ASYNC_RETURN(double) NTgCalls::cpuUsage() const {
        SMART_ASYNC(this)
        return hardwareInfo->getCpuUsage();
        END_ASYNC
    }

    ASYNC_RETURN(std::map<int64_t, Stream::Status>) NTgCalls::calls() {
        SMART_ASYNC(this)
        std::map<int64_t, Stream::Status> statusList;
        std::lock_guard lock(mutex);
        for (const auto& [fst, snd] : connections) {
            statusList.emplace(fst, snd->status());
        }
        return statusList;
        END_ASYNC
    }

    void NTgCalls::remove(const int64_t chatId) {
        RTC_LOG(LS_INFO) << "Removing call " << chatId << ", Acquiring lock";
        std::lock_guard lock(mutex);
        RTC_LOG(LS_INFO) << "Lock acquired, removing call " << chatId;
        if (!exists(chatId)) {
            RTC_LOG(LS_ERROR) << "Call " << chatId << " not found";
            THROW_CONNECTION_NOT_FOUND(chatId)
        }
        connections.erase(connections.find(chatId));
        RTC_LOG(LS_INFO) << "Call " << chatId << " removed";
    }

    bool NTgCalls::exists(const int64_t chatId) const {
        return connections.contains(chatId);
    }

    CallInterface* NTgCalls::safeConnection(const int64_t chatId) {
        std::lock_guard lock(mutex);
        if (!exists(chatId)) {
            THROW_CONNECTION_NOT_FOUND(chatId)
        }
        return connections[chatId].get();
    }

    Protocol NTgCalls::getProtocol() {
        return {
            92,
            92,
            true,
            true,
            signaling::Signaling::SupportedVersions(),
        };
    }

    template<typename DestCallType, typename BaseCallType>
    DestCallType* NTgCalls::SafeCall(BaseCallType* call) {
        if (!call) {
            return nullptr;
        }
        if (auto* derivedCall = dynamic_cast<DestCallType*>(call)) {
            return derivedCall;
        }
        throw ConnectionError("Invalid call type");
    }

    std::string NTgCalls::ping() {
        return "pong";
    }
} // ntgcalls