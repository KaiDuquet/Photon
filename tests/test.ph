struct Token {
    type: int;
    union val {
        _int: int;
        _float: float;
        _string: string;
        name: string;
    }
}

function ph_main(source_path: string) {
    code := filehandle.read_file(source_path);
    if (code.isspace() || code == "") {
        return;
    }
    phlex.init(sourcepath, code);
    while (phlex.token != phtoken.TOKEN_EOF) {
        phprint.print_decl(phparser.parse_decl());
        print();
    }
}

function main(argc: int, argv: string[]) {
    file_name := argv[0];
    if (argc <= 1) {
        print("For now, there is no working REPL.");
        exit(0);
    }
    source_file := argv[1];
    ph_main(source_file);
}
