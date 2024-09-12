//
// Created by Laky64 on 19/08/2023.
//

#pragma once

#include "tracks/video_track_source.hpp"
#include "../../models/i420_image_data.hpp"
#include "../peer_connection/peer_connection_factory.hpp"

namespace wrtc {

    class RTCVideoSource {
    public:
        RTCVideoSource();

        ~RTCVideoSource();

        [[nodiscard]] rtc::scoped_refptr<webrtc::VideoTrackInterface> createTrack() const;

        void OnFrame(const i420ImageData& data, int64_t absolute_capture_timestamp_ms) const;

    private:
        rtc::scoped_refptr<VideoTrackSource> source;
        rtc::scoped_refptr<PeerConnectionFactory> factory;
    };

} // wrtc
