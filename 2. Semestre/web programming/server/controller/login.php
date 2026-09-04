<?php

header('Access-Control-Allow-Origin: *);
header('Access-Control-Allow-Headers: *);
// captura o post e transforma o json em array
$jsonInput = file_get_contents("php://input");
$data = json_decode($jsonInput, true)

// acessa o array e pega o valor do nome e senha
$username = data["nome"] ?? "sem nome";
$password = data["senha"] ?? "sem senha";

/*
"timestamp"=>
*/

// acessando o json
$arrayData = [
    "timestamp"=> date("Y-m-d H:i:s"),
    "username"=> $username,
    "password"=> sha1($password),
];

// transforma o array em json
$jsonString = json_encode($arrayData, JSON_PRETTY_PRINT);
file_put_contents("dados.json", $jsonString);
