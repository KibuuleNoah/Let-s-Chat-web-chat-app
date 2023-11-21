const giveMessageDirection = (id1,id2) => id1 == id2 ? "end" : "start"

id1 = 577,id2 = 570

console.log(giveMessageDirection(id1,id2))

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Image Resize</title>
</head>
<body>
  <input type="file" id="imageInput" accept="image/*">
  <canvas id="resizedCanvas" width="200" height="200" style="border:1px solid #000;"></canvas>

  <script>
    document.getElementById('imageInput').addEventListener('change', handleImage);

    function handleImage() {
      const input = document.getElementById('imageInput');
      const canvas = document.getElementById('resizedCanvas');
      const ctx = canvas.getContext('2d');

      const img = new Image();
      img.src = URL.createObjectURL(input.files[0]);

      img.onload = function() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, 200, 200);
      };
    }
  </script>
</body>
</html>




document.addEventListener('DOMContentLoaded', function () {
    // Replace 'yourImagePath' with the actual file path
    var imagePath = '/path/to/your/image.jpg';
    
    var canvas = document.getElementById('imageCanvas');
    var ctx = canvas.getContext('2d');
    
    var img = new Image();
    
    img.onload = function () {
        // Resize the image to fit the canvas
        var aspectRatio = img.width / img.height;
        var maxWidth = canvas.width;
        var maxHeight = canvas.height;
        var newWidth = maxWidth;
        var newHeight = maxWidth / aspectRatio;
    
        if (newHeight > maxHeight) {
            newHeight = maxHeight;
            newWidth = maxHeight * aspectRatio;
        }
    
        // Draw the resized image on the canvas
        ctx.drawImage(img, 0, 0, newWidth, newHeight);
    };
    
    // Set the image source to the provided file path
    img.src = imagePath;
});
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Resizer</title>
</head>
<body>
    <canvas id="imageCanvas" width="400" height="300" style="border:1px solid #000;"></canvas>
    <script src="app.js"></script>
</body>
</html>

