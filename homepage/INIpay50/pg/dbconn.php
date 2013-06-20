<?php
$dbconn = pg_connect("host=localhost dbname=gift user=gift password=reverse90");
pg_set_client_encoding($dbconn, "euc-kr");
if(!$dbconn){
	echo("DB접속 실패!");
	exit();
}


function fetch_one($sql){
	global $dbconn;
	$result = pg_query($dbconn, $sql);
	if(!$result)
	throw new Exception("잘못된 쿼리입니다.");

	if(pg_num_rows($result)==0)
	throw new Exception("결과가 없습니다.");
	
	return pg_fetch_object($result);
}

?>
