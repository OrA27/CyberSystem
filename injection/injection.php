<?php
  $os = php_uname();
  if (strtoupper(substr($os, 0, 3)) === 'WIN') {
    $output = shell_exec('dir');
  } else {
    if (strtoupper(substr($os, 0, 5)) === 'LINUX') {
      $output = shell_exec('ls');
    } else {
      $output = 'unkown os, injection.php';
    }
  }
  echo $output;
  //$output = shell_exec('cmd \k');
  //$output = shell_exec('dir ..');
  //echo $output;
?>