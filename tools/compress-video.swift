// Re-encode a video for the web: H.264, no audio, explicit size and bitrate.
// Usage: swift tools/compress-video.swift <in.mp4> <out.mp4> <width> <height> <bitrate_kbps>
import AVFoundation
import Foundation

let args = CommandLine.arguments
guard args.count == 6, let w = Int(args[3]), let h = Int(args[4]), let kbps = Int(args[5]) else {
    FileHandle.standardError.write("usage: compress-video.swift in out width height kbps\n".data(using: .utf8)!)
    exit(2)
}
let inURL = URL(fileURLWithPath: args[1])
let outURL = URL(fileURLWithPath: args[2])
try? FileManager.default.removeItem(at: outURL)

let asset = AVURLAsset(url: inURL)
guard let track = asset.tracks(withMediaType: .video).first else { print("no video track"); exit(1) }

let reader = try AVAssetReader(asset: asset)
let readerOutput = AVAssetReaderTrackOutput(track: track, outputSettings: [
    kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_420YpCbCr8BiPlanarVideoRange
])
readerOutput.alwaysCopiesSampleData = false
reader.add(readerOutput)

let writer = try AVAssetWriter(outputURL: outURL, fileType: .mp4)
let settings: [String: Any] = [
    AVVideoCodecKey: AVVideoCodecType.h264,
    AVVideoWidthKey: w,
    AVVideoHeightKey: h,
    AVVideoScalingModeKey: AVVideoScalingModeResizeAspectFill,
    AVVideoCompressionPropertiesKey: [
        AVVideoAverageBitRateKey: kbps * 1000,
        AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
        AVVideoMaxKeyFrameIntervalKey: 60,
        AVVideoAllowFrameReorderingKey: true,
        AVVideoExpectedSourceFrameRateKey: Int(track.nominalFrameRate.rounded()),
    ],
]
let input = AVAssetWriterInput(mediaType: .video, outputSettings: settings)
input.expectsMediaDataInRealTime = false
input.transform = track.preferredTransform
writer.add(input)
writer.shouldOptimizeForNetworkUse = true

guard writer.startWriting(), reader.startReading() else {
    print("start failed:", writer.error ?? "", reader.error ?? ""); exit(1)
}
writer.startSession(atSourceTime: .zero)

let queue = DispatchQueue(label: "encode")
let done = DispatchSemaphore(value: 0)
var frames = 0
input.requestMediaDataWhenReady(on: queue) {
    while input.isReadyForMoreMediaData {
        if let sb = readerOutput.copyNextSampleBuffer() {
            input.append(sb); frames += 1
        } else {
            input.markAsFinished()
            writer.finishWriting { done.signal() }
            return
        }
    }
}
done.wait()
if writer.status == .completed {
    let size = (try? FileManager.default.attributesOfItem(atPath: outURL.path)[.size] as? Int) ?? 0
    print("ok frames=\(frames) bytes=\(size) (\(size / 1024) KB) \(w)x\(h) @ \(kbps) kbps")
} else {
    print("failed:", writer.error ?? "unknown"); exit(1)
}
