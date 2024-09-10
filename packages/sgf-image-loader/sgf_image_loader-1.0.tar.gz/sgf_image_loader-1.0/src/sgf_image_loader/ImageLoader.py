from PIL import Image

import struct
import gzip

class ImageLoader:
    @staticmethod
    def load_image(file_path: str) -> Image:        
        with open(file_path, "rb") as binary_file:
            data = gzip.decompress(binary_file.read())
            
            return ImageLoader.construct_image(data)
        
        return None
    
    @staticmethod
    def construct_image(data: bytes) -> Image:
        # bit pointer
        bp = 0
        
        def get_bytes(format) -> bytes:
            nonlocal bp
            size = struct.calcsize(format)
            out = struct.unpack(format, data[bp:bp+size])
            bp += size
            return out
        
        image = None
        
        # --- Header --- #
        image_size = get_bytes('HH')
        
        # load color dict
        dict_size = get_bytes("B")[0]
        colors = []
        
        for i in range(dict_size):
            colors.append(get_bytes('4B'))
        
        # --- Body --- #
        new_data = []
        
        reps = 0
        i = 0
        
        # get each repetition # and pixel value
        while i < image_size[0] * image_size[1]:
            reps = get_bytes('B')[0]
            color = colors[get_bytes('B')[0]]
            
            for rep in range(reps):
                new_data.append(color)
            i += reps
        
        image = Image.new("RGBA", image_size, "#000")
        image.putdata(new_data)
        
        return image
    
    @staticmethod
    def save_as_sgf(file_path: str, target_path: str) -> None:
        with Image.open(file_path) as image:
            with open(target_path, "wb") as binary_file:
                # --- Header --- #
                # image size
                data = bytes()
                data += struct.pack("HH", image.size[0], image.size[1])
                
                # color dictionary
                color_dict = {}
                dict_bytes = bytes()
                curr_key = 0
                
                for color in image.getdata():
                    if color in color_dict:
                        continue
                    color_dict[color] = curr_key
                    curr_key += 1
                    
                    dict_bytes += color[0].to_bytes(1)
                    dict_bytes += color[1].to_bytes(1)
                    dict_bytes += color[2].to_bytes(1)
                    dict_bytes += color[3].to_bytes(1)
                
                data += curr_key.to_bytes(1)
                data += dict_bytes
                
                # --- Body --- # 
                # load pixels from color_dict
                reps = 1
                last = None
                
                for color in image.getdata():
                    if reps == 255:
                        data += reps.to_bytes(1)
                        data += color_dict[last].to_bytes(1)
                        reps = 1
                        last = None
                    
                    if last == None:
                        last = color
                        continue
                    elif last == color:
                        reps += 1
                        continue
                    else:
                        data += reps.to_bytes(1)
                        data += color_dict[last].to_bytes(1)
                        reps = 1
                    
                    last = color
                
                data += reps.to_bytes(1)
                data += color_dict[last].to_bytes(1)
                
                binary_file.write(gzip.compress(data))
