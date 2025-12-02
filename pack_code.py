import os

# 设置不需要处理的文件夹（黑名单）
IGNORE_DIRS = {'.git', 'venv2.0', '__pycache__', 'ai_assistant.egg-info', '.idea', '.vscode'}
# 设置需要读取的文件后缀
TARGET_EXTS = {'.py', '.md', '.txt', '.jsonl', '.gitignore'}
# 输出文件名
OUTPUT_FILE = 'all_project_code.txt'

def merge_files():
    current_dir = os.getcwd()
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        # 遍历目录
        for root, dirs, files in os.walk(current_dir):
            # 排除黑名单目录，修改 dirs 列表会影响 os.walk 的后续遍历
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            for file in files:
                file_ext = os.path.splitext(file)[1]
                # 跳过脚本自己和输出文件
                if file == 'pack_code.py' or file == OUTPUT_FILE:
                    continue
                
                # 只处理指定后缀的文件
                if file_ext in TARGET_EXTS or file == 'LICENSE': # LICENSE 也带上
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, current_dir)
                    
                    try:
                        print(f"正在处理: {rel_path}")
                        # 写入文件分隔符和文件名，方便 AI 识别
                        outfile.write(f"\n{'='*20}\n")
                        outfile.write(f"FILE_START: {rel_path}\n")
                        outfile.write(f"{'='*20}\n\n")
                        
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                            outfile.write(infile.read())
                            
                        outfile.write(f"\n\nFILE_END: {rel_path}\n")
                    except Exception as e:
                        print(f"跳过文件 {rel_path}: {e}")

    print(f"\n✅ 完成！所有代码已合并到: {OUTPUT_FILE}")
    print("请将该文件发送给 AI。")

if __name__ == '__main__':
    merge_files()