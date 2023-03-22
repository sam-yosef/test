
import ffmpeg

def compress_video(input_file, output_file, codec='libx265', crf=28):
    try:
        input_stream = ffmpeg.input(input_file)
        output_stream = input_stream.output(output_file, codec=codec, crf=crf)
        ffmpeg.run(output_stream)
        return output_file
    except Exception as e:
        raise RuntimeError(f"An error occurred while compressing the video: {e}")
