<?php
$dbconn = pg_connect("host=localhost dbname=gift user=gift password=reverse90");
pg_set_client_encoding($dbconn, "euc-kr");
if(!$dbconn){
	echo("DB���� ����!");
	exit();
}


function fetch_one($sql){
	global $dbconn;
	$result = pg_query($dbconn, $sql);
	if(!$result)
	throw new Exception("�߸��� �����Դϴ�.");

	if(pg_num_rows($result)==0)
	throw new Exception("����� �����ϴ�.");
	
	return pg_fetch_object($result);
}

?>
