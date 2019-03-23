if ($args.Count -gt 1) {
    $args = ""
}

python.exe .\wdc\wdc.py $args
