import os
import rawpy
from PIL import Image
from datetime import datetime
import argparse

convertedcount = 0

def convert_arw_to_jpeg(arw_file_path, output_folder, date_folder):
    global convertedcount  # This is required to modify the global variable
    with rawpy.imread(arw_file_path) as raw:
        convertedcount += 1
        rgb_image = raw.postprocess()
        pil_image = Image.fromarray(rgb_image)
        
        # Generate the base filename and output path
        base_filename = os.path.splitext(os.path.basename(arw_file_path))[0]
        output_path = os.path.join(output_folder, date_folder, base_filename + '.jpg')

        # Create the folder for the date if it doesn't exist
        os.makedirs(os.path.join(output_folder, date_folder), exist_ok=True)

        # Save the image as a JPEG
        pil_image.save(output_path, 'JPEG')
        print(f"Converted {arw_file_path} to {output_path}")

def convert_all_arw_in_folder(input_folder, output_folder):
    arw_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.arw')]
    arw_files.sort(key=lambda f: os.path.getctime(os.path.join(input_folder, f)))
    for filename in arw_files:
        arw_file_path = os.path.join(input_folder, filename)
        
        # Get the creation time of the ARW file
        creation_time = os.path.getctime(arw_file_path)
        
        # Format the creation time as DD-MM-YYYY
        date_folder = datetime.fromtimestamp(creation_time).strftime('%d-%m-%Y')
        
        # Convert the ARW file to JPEG and organize by the ARW file's creation date
        convert_arw_to_jpeg(arw_file_path, output_folder, date_folder)

def main():
    print("arw to jpg by Sukimasai")
    parser = argparse.ArgumentParser(description='Convert ARW files to JPEG.')
    parser.add_argument('input_folder', type=str, help='Input folder with ARW files')
    parser.add_argument('output_folder', type=str, help='Output folder to save JPEGs')
    args = parser.parse_args()

    convert_all_arw_in_folder(args.input_folder, args.output_folder)

    # Print count after conversion
    print(f"Done converted {convertedcount} files")

if __name__ == "__main__":
    main()
