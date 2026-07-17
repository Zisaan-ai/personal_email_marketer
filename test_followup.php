<?php
$output = shell_exec("cd /home/terapkco/xcomic_backend; /home/terapkco/virtualenv/xcomic_backend/3.11/bin/python test_followup.py 2>&1");
echo "<pre>" . htmlspecialchars($output) . "</pre>";
?>
