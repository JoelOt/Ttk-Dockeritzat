<?php
include("db.php"); //include aplica el codi de l'arxiu que dius, aquest obre la db

$requestUri = $_SERVER['REQUEST_URI'];  //agafem la url de la request
$parts = explode('/', $requestUri);  //separem per parts i ens quedem amb la última, sera ex: timetables?day=Fri&hour=8:00
$parts = array_filter($parts);
$parts = end($parts);
$parts = explode('?', $parts);  //separem i agafem la part abans de "="
$route = $parts[0];

switch ($route) {  //triem entre els diferents casos:
    case 'uid':
        if(isset($_SERVER['HTTP_UID'])){    //el uid el passem a la capçalera de la solicitud, en get dona error quan no hi ha restriccions al url
            $uid = $_SERVER['HTTP_UID'];    //d'aquesta manera podem recuperar el seu valor
            $consulta = "SELECT userName FROM students WHERE `uid` = '$uid'";  //agafem el userName de la persona corresponent i l'enviem al client en format json
        };
        break; //no passarà mai desde el nostre client
    case 'timetables':
        $consulta = "SELECT * FROM timetables";  //la consulta ha de retornar tota la llista timetables seguint les restriccions esmentades
        if(isset($_GET['day'])){  //comprovem si ha posat dia a la request i en cas positiu el guardem i creeem una restricció mysql
            $day = $_GET['day'];
            $consulta .= " WHERE day = '$day'";  //estem assumient que no es pot especificar hour sense abans day
            if(isset($_GET['hour'])){
                $hour = $_GET['hour'];
                $consulta .= " AND hour = '$hour'";
            }
        }if(isset($_GET['limit'])){  //limit ya ve donat per la sintaxis mysql i limita el nombre de files que pot tenir la resposta
            $limit = $_GET['limit'];
            $consulta .= " LIMIT $limit"; 
        }
        break;
    case 'tasks':
        $consulta = "SELECT * FROM tasks"; 
        if(isset($_GET['date'])){
            $date = $_GET['date'];
            if($date = "now"){
                $consulta .= " WHERE date = CURRENT_DATE";  //CURRENT_DATE es una paraula reservada de mysql que dona la data d'avui 
            }else{
                $consulta .= " WHERE date = '$date'";
            }
        }
        $consulta .= " ORDER BY date";  //ha d'anar aqui per seguir l'ordre establert a les sentències mysql
        if(isset($_GET['limit'])){
            $limit = $_GET['limit'];
            $consulta .= " LIMIT $limit"; 
        }
            break;
    case 'marks':
        if(isset($_SERVER['HTTP_UID'])){
            $uid = $_SERVER['HTTP_UID'];    
            $consulta = "SELECT subject,name,mark FROM marks WHERE id = '$uid'";  //restringim al uid
        }
        if(isset($_GET['subject'])){
            $subject = $_GET['subject'];
            $consulta .= " AND subject = '$subject'";
        }if (isset($_GET['mark']['lt'])) {  //no entenc la tria [lt] per denominar less than, segon he investigat no és una forma recurrent indicar-ho entre [] i genera problemes
            $mark = $_GET['mark']['lt'];
            $consulta .= " AND mark < '$mark'";  //retorna les marks < al valor esmentat
        }
        break;
    default:
        echo "error en l'url";  //hi ha un error en l'url ja que no és cap cas del switch
        exit();
    }
    $result = mysqli_query($conn, $consulta);  //executa la consulta $consulta a la db $conn
    $data= array(); //l'inicialitzem com un array buit
    while($row = mysqli_fetch_assoc($result)){  //anem recollint els arrays de les diferents columnes i fent un array de arrays, és a dir, una matriu
        $data[] = $row;
    }
    header('Content-Type: application/json');  //indiquem a la capçalera que les dades son en foramt json
    echo json_encode($data);    //les enviem al client codificades en aquest format
?>
