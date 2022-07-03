write-host("===== CREATE A NEW PROJECT =====");
$projectname = read-host("Project name");
if (test-path $projectname) {
    write-host "Project '$projectname' already exists!";
    write-host "===== PROCESS ENDED =====";
    Exit
}
$authors_str = read-host("Authors names (separated by ',')");
$director = read-host("Director");
$production = read-host("Production name");
$authors_list = $authors_str.split(",") | Foreach-Object -Process {$_.trim()};
$date = get-date -Format "dd/MM/yyyy";
write-host("= Creating the project directory =");
$null = mkdir $projectname;
write-host("= Creating metadata file =");
$metadata = @{"name"=$projectname;"authors"=$authors_list;"director"=$director;"creation-date"=$date;"production"=$production};
$json = ($metadata | ConvertTo-Json -Depth 99);
$Utf8NoBomEncoding = New-Object System.Text.UTF8Encoding $False;
$meta_path = (get-location).Path + "/" + $projectname + "/metadata.json";
[System.IO.File]::WriteAllLines($meta_path, $json, $Utf8NoBomEncoding);
write-host("===== PROCESS ENDED =====");
