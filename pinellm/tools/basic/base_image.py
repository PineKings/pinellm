import base64
#  base 64 编码格式
def encode_image(image_path):
    """传入图片路径，返回base64编码的图片数据
    
    参数：
      - image_path: 图片路径
    """
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        # 获取图片的 MIME 类型
        if image_path.lower().endswith(".jpg"):
            data_type = "image/jpeg" 
        elif image_path.lower().endswith(".png"): 
            data_type = "image/png"
        elif image_path.lower().endswith(".webp"): 
            data_type = "image/webp"
        else:
            raise ValueError("不支持图片格式")
        # 返回 base64 编码的图片数据
        return f"data:{data_type};base64,{encoded_image}"