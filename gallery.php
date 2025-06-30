<!DOCTYPE html>
<html>
<head>
  <title>ESP32-CAM Photo Gallery</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    .flex-container {
      display: flex;
      flex-wrap: wrap;
    }
    .flex-container > div {
      text-align: center;
      margin: 10px;
    }
  </style>
</head><body>
<h2>ESP32-CAM Photo Gallery</h2>
<?php
  // Image extensions
  $image_extensions = array("png","jpg","jpeg","gif");

  // Check delete HTTP GET request - remove images
  if(isset($_GET["delete"])){
    $imageFileType = strtolower(pathinfo($_GET["delete"],PATHINFO_EXTENSION));
    if (file_exists($_GET["delete"]) && ($imageFileType == "jpg" ||  $imageFileType == "png" ||  $imageFileType == "jpeg") ) {
      echo "File found and deleted: " .  $_GET["delete"];
      unlink($_GET["delete"]);
    }
    else {
      echo 'File not found - <a href="gallery.php">refresh</a>';
    }
  }
  // Target directory
$count = 1;
$datum = mktime(date('H')+0, date('i'), date('s'), date('m'), date('d'), date('y'));
date_default_timezone_set('Asia/Jakarta');
$dir  = "uploads/". date('Y.m.d', $datum)."/";
// $dir  = "uploads/2025.05.04/";
  if (is_dir($dir)){
    echo '<div class="flex-container">';
    $files = scandir($dir);
    rsort($files);
    $count=0;
    for ($i = 0; $i < count($files); $i++) {
        $file = $files[$i];
      if ($file != '.' && $file != '..') {?>
        <div>
          <p><a href="gallery.php?delete=<?php echo $dir . $file; ?>">Delete file</a> - <?php echo $file; ?></p>
          <a href="<?php echo $dir . $file; ?>">
            <img src="<?php echo $dir . $file; ?>" style="width: 350px;" alt="" title=""/>
          </a>
       </div>
<?php
$i+=100;
$count++;
      }
      if($count==20){
          break;
      }
    }
  }
  if($count==1) { echo "<p>No images found</p>"; } 
?>
  </div>
</body>
</html>
