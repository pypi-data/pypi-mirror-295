import os
import shutil
import argparse

def extract_mp4_files(source_dir, destination_dir):
    # ディレクトリが存在しない場合は作成
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    
    # ソースディレクトリ内のすべてのファイルをチェック
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith('.mp4'):
                # MP4ファイルをコピー
                source_file = os.path.join(root, file)
                destination_file = os.path.join(destination_dir, file)
                shutil.copy2(source_file, destination_file)
                print(f'Copied: {source_file} to {destination_file}')


def main():
    parser = argparse.ArgumentParser(description='Extract MP4 files from source directory to destination directory.')
    parser.add_argument('source_dir', type=str, help='The source directory to search for MP4 files.')
    parser.add_argument('destination_dir', type=str, help='The destination directory to copy MP4 files to.')
    
    args = parser.parse_args()
    
    extract_mp4_files(args.source_dir, args.destination_dir)

if __name__ == '__main__':
    main()