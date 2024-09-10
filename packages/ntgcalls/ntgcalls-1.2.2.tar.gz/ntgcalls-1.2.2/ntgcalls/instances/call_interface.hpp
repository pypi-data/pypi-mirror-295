//
// Created by Laky64 on 15/03/2024.
//

#pragma once
#include <memory>

#include "ntgcalls/stream.hpp"

namespace ntgcalls {

    class CallInterface {
        bool connected = false;
        std::atomic_bool isExiting;

        void cancelNetworkListener();

    public:
        enum class ConnectionState {
            Connecting = 1 << 0,
            Connected = 1 << 1,
            Failed = 1 << 2,
            Timeout = 1 << 3,
            Closed = 1 << 4
        };
    protected:
        std::mutex mutex;
        std::unique_ptr<wrtc::NetworkInterface> connection;
        std::unique_ptr<Stream> stream;
        wrtc::synchronized_callback<ConnectionState> connectionChangeCallback;
        rtc::Thread* updateThread;
        std::unique_ptr<rtc::Thread> networkThread;

        void setConnectionObserver();

    public:
        explicit CallInterface(rtc::Thread* updateThread);

        virtual ~CallInterface();

        enum class Type {
            Group = 1 << 0,
            Outgoing = 1 << 1,
            Incoming = 1 << 2,
            P2P = Outgoing | Incoming
        };

        bool pause() const;

        bool resume() const;

        bool mute() const;

        bool unmute() const;

        void changeStream(const MediaDescription& config) const;

        void onStreamEnd(const std::function<void(Stream::Type)> &callback);

        void onConnectionChange(const std::function<void(ConnectionState)> &callback);

        uint64_t time() const;

        MediaState getState() const;

        Stream::Status status() const;

        virtual Type type() const = 0;

        template<typename DestCallType, typename BaseCallType>
        static DestCallType* Safe(const std::unique_ptr<BaseCallType>& call) {
            if (!call) {
                return nullptr;
            }
            if (auto* derivedCall = dynamic_cast<DestCallType*>(call.get())) {
                return derivedCall;
            }
            throw std::runtime_error("Invalid NetworkInterface type");
        }
    };

    inline int operator&(const CallInterface::Type& lhs, const CallInterface::Type rhs){
        return static_cast<int>(lhs) & static_cast<int>(rhs);
    }
} // ntgcalls
