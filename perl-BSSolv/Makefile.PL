use ExtUtils::MakeMaker;
WriteMakefile(
    NAME         => 'BSSolv',
    VERSION_FROM => 'BSSolv.pm',
    INC          => '-I/usr/include/solv',   # e.g., '-lm'
    LIBS         => ['-Llibsolv/src -Llibsolv/ext -lsolvext -lsolv -lz -llzma'],   # e.g., '-lm'
)
