<?php
    
    //create a JSON object
    $myJSON = new stdClass();
   
    //_POST[] reads the input variable from HTML
    //Populating the JSON object with input data from HTML form
    $myJSON->website = $_POST['website'];
    $myJSON->showscrape = $_POST["scrapedata"];
    
    //Create a file called data.json from json object. File is saved in home folder called "sites"
    file_put_contents("data.json", json_encode($myJSON,true));

    //logic to launch the main python file via shell command
    $command = escapeshellcmd('python3 processwebsite.py');
    $output = shell_exec($command);
    
    //if input form has a flag set to true to show website scrapte data, then read scrape.txt, else do not
    //once file is read via the fopen command, then read , display via echo command, then close the file
    if ($_POST["website"]=="nytimes")
    { 
        echo "The website chosen is New York Times";
    }
    if ($_POST["website"]=="foxnews")
    {
        echo "The website chosen is Fox News";
    }
    if($_POST["scrapedata"]=="true")
    {
        $myfile = fopen("scrape.txt", "r") or die("Unable to open file!");
        echo fread($myfile,filesize("scrape.txt"));
        fclose($myfile);
    }

    //logic to display the top words via reading the topwords file, then display and close the file
    $myfile = fopen("topwords.txt", "r") or die("Unable to open file!");
    echo fread($myfile,filesize("topwords.txt"));
    fclose($myfile);

    //logic to display the top words via reading the sentiment file, then display via echo command and close the file
    $myfile = fopen("sentiment.txt", "r") or die("Unable to open file!");
    echo fread($myfile,filesize("sentiment.txt"));
    fclose($myfile);
    
    
    echo " There are 3 main classes of sentiment (positive, negative, and neutral), which are on a 0-1 scale. ";
    echo " The compound score is the sum of positive, negative & neutral scores which is then normalized between -1(most extreme negative) and +1 (most extreme positive). ";
?>