#!/usr/bin/env bash

# set -x # echo all commands executed

function error () {
  tput setaf 1; echo "ERROR; $@" 1>&2; tput sgr0
}

function warning () {
  tput setaf 3; echo "WARNING; $@" 1>&2; tput sgr0
}

function info () {
  tput setaf 2; echo -n "INFO; "; tput sgr0; echo "$@"
}

info "Working in dir: `pwd`"

usage_exit() {
  echo -e "
Usage:\t$0 [OPTIONS]
Options:
  -s, --setup STAGE\tSTAGE用のdockerイメージを起動する
    STAGE: WALLE_PRODUCTION_STAGE (環境変数に書き込む)
  -r, --restart SERVICE\t既存のSERVICEを再起動する
  -t, --stop SERVICE\t既存のSERVICEを停止する
  -l, --logs SERVICE\t既存のSERVICEのログを表示
    SERVICE:
    -f, --frontend\tfrontend(vuejs)
    -b, --backend\tbackend(responder)
    --nginx\tNGINX
    --db\tmysql(dev環境のみ)
  -d, --db COMMAND\tEdit Database
    COMMAND:
    init\tInitialize all data in Database
    show\tShow all data in Database
" 1>&2
  exit 1
}

service=''

while getopts fbrdi-: opt; do
  optarg="${!OPTIND}"
  [[ x"$opt" = x- ]] && opt="-$OPTARG"

  case "-$opt" in
    -f|--frontend)
      bash -c "npm run serve"
      ;;
    -b|--backend)
      bash -c "npm run build"
      ;;
    -r|--run)
      bash -c "python run.py"
      ;;
    --protoc)
      protoc=true
      ;;
    -d|--db)
      dbcommand="$optarg"
      shift
      ;;
    -i|--internationalization)
      bash -c "python edit.py --lang"
      ;;
    --)
      break
      ;;
    -\?)
      usage_exit
      exit 1
      ;;
    --*)
      echo "$0 illegal option -- ${opt##-}" >&2
      usage_exit
      exit 1
      ;;
  esac
done
shift $((OPTIND - 1))

function build_protobuf() {
  CWD=$(pwd)
  PROTO_DIR="$CWD"/protobuf
  pb2=compiled_pb2
  cd "$PROTO_DIR"
  protofiles=$(command ls -a | grep '.proto')
  # Compile protobuf (python)
  AUTOGEN_PY=../protobuf
  info "Compiling protobuf for python to $PROTO_DIR/$AUTOGEN_PY/$pb2.py"
  mkdir -p "$AUTOGEN_PY"
  [ $(command find "$AUTOGEN_PY" -name '*_pb2*' | wc -l) -gt 0 ] && rm "$AUTOGEN_PY"/*_pb2*
  protoc --python_out="$AUTOGEN_PY" --mypy_out="$AUTOGEN_PY" *.proto
  echo '# pylint: skip-file' > "$AUTOGEN_PY"/$pb2.py
  for f in $protofiles; do
    F="${f%.*}" && echo "from .${F}_pb2 import * # noqa" >> "$AUTOGEN_PY"/$pb2.py
  done

  # Compile protobuf (typescript)
  if [[ x"$backonly" != xtrue ]]; then
    cd "$PROTO_DIR"
    AUTOGEN_TS=../src/plugins/protobuf
    mkdir -p "$AUTOGEN_TS"
    [ $(command find "$AUTOGEN_TS" -name '*_pb2*' | wc -l) -gt 0 ] && rm "$AUTOGEN_TS"/*_pb2*
    info "Compiling protobuf for js/ts to $PROTO_DIR/$AUTOGEN_TS/$pb2.ts"
    protoc \
      --plugin=$CWD/node_modules/.bin/protoc-gen-ts_proto \
      --ts_proto_opt=exportCommonSymbols=false,unrecognizedEnum=false,fileSuffix=_pb2,esModuleInterop=true,oneof=unions \
      --ts_proto_out="$AUTOGEN_TS" *.proto
    echo '/* eslint-disable */' > "$AUTOGEN_TS"/$pb2.ts
    for f in $protofiles; do
      F="${f%.*}" && echo "export * from './${F}_pb2';" >> "$AUTOGEN_TS"/$pb2.ts
    done
  fi
  cd "$CWD"
  # Create a documentation of protobuf defined APIs
  # docker run --rm \
  #     -v $PWD/docs:/out \
  #     -v $PWD/protobuf:/protos/protobuf \
  #     pseudomuto/protoc-gen-doc --doc_opt=markdown,protobuf.md protobuf/*.proto
}

if [[ x$protoc = xtrue ]]; then
  build_protobuf
fi

if [[ x$pipenvlock = xtrue ]]; then
  pipenv lock
fi

if [[ x$dbcommand != x ]]; then
  python edit.py -d $dbcommand
fi

