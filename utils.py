
import ffmpeg

def compress_video(input_path, output_path, codec='libx265', crf=28, preset='medium', resolution=None):
    
    try:
        if resolution:
            width, height = resolution.split('x')
            resolution = {'width': int(width), 'height': int(height)}

        input_stream = ffmpeg.input(input_path)

        extra_args = {}
        if resolution:
            extra_args['size'] = resolution
        
        output_stream = (
            input_stream
            .video.filter('scale', **extra_args)
            .output(
                output_path,
                vcodec=codec,
                crf=crf,
                preset=preset
            )
        )
        ffmpeg.run(output_stream)
        
    except Exception as e:
        print('Error while compressing video:', e)
