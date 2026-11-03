
import gradio as gr
import subprocess
import os
import tempfile

def upscale_video(video_path, resolution):
    if not video_path:
        raise gr.Error("Please upload a video first.")

    output_dir = tempfile.mkdtemp()
    output_path = os.path.join(output_dir, "upscaled_video.mp4")

    if resolution == "4K":
        size = "3840"
    else:
        size = "2560"

    command = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf",
        f"scale='if(gte(iw,ih),{size},-2)':'if(gte(iw,ih),-2,{size})':flags=lanczos",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "20",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        output_path
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise gr.Error("Video processing failed. Check FFmpeg installation.")

    return output_path


with gr.Blocks(title="AI Video Upscaler") as app:
    gr.Markdown("# AI Video Upscaler")
    gr.Markdown("Enhance your videos and export in high resolution.")

    video_input = gr.Video(label="Upload your video")

    resolution = gr.Radio(
        choices=["2K", "4K"],
        value="4K",
        label="Choose output resolution"
    )

    process_button = gr.Button("Upscale Video", variant="primary")

    video_output = gr.Video(label="Processed video")

    process_button.click(
        fn=upscale_video,
        inputs=[video_input, resolution],
        outputs=video_output
    )

app.launch()
