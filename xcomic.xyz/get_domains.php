<?php
try {
    $db = new PDO('sqlite:/home/terapkco/xcomic_backend/sql_app.db');
    $stmt = $db->query('SELECT email FROM sending_accounts WHERE is_active=1');
    $accounts = $stmt->fetchAll(PDO::FETCH_ASSOC);
    echo json_encode($accounts);
} catch (Exception $e) {
    echo json_encode(['error' => $e->getMessage()]);
}
?>