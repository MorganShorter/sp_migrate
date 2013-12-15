#!/bin/bash

##### START CONFIG ######
# NONE OF THIS WORKS SO DONT BOTHER CONFIGURING IT





# SCHEMA OPTIONS #
# Include indexes? (y/n)
SCHEMA_INDEXES="y"
# Include not null constraints? (y/n)
SCHEMA_NOTNULL="y"
# Include relations (fk contraints)? (y/n)
SCHEMA_RELATIONS="n"
# Include DROP TABLE statements? (y/n)
SCHEMA_DROPTABLE="n"
###### END CONFIG ########

SCHEMA_OPTIONS=""
if [[ "$SCHEMA_INDEXES" == "y" || "$SCHEMA_INDEXES" == "Y" ]]; then
  SCHEMA_OPTIONS="--indexes"
else
  SCHEMA_OPTIONS="--no-indexes"
fi

if [[ "$SCHEMA_NOTNULL" == "y" || "$SCHEMA_NOTNULL" == "Y" ]]; then
  SCHEMA_OPTIONS="$SCHEMA_OPTIONS --not-null"
else
  SCHEMA_OPTIONS="$SCHEMA_OPTIONS --no-not-null"
fi

if [[ "$SCHEMA_RELATIONS" == "y" || "$SCHEMA_RELATIONS" == "Y" ]]; then
  SCHEMA_OPTIONS="$SCHEMA_OPTIONS --relations"
else
  SCHEMA_OPTIONS="$SCHEMA_OPTIONS --no-relations"
fi

if [[ "$SCHEMA_DROPTABLE" == "y" || "$SCHEMA_DROPTABLE" == "Y" ]]; then
  SCHEMA_OPTIONS="$SCHEMA_OPTIONS --drop-table"
else
  SCHEMA_OPTIONS="$SCHEMA_OPTIONS --no-drop-table"
fi

MODE="$1"
DATABASE="$2"

#Internal Field Seperator - so we can iterate through space containing table names
IFS=$'\012'

shift 2


function get_spec_tables()
{
  local counter=0
  local db="$1"
  shift
  local current_param="$1"
  local SPEC_TABLES=""
  local tables=$(get_tables "$db")
  while [[ "$current_param" != "" ]]; do
    if [[ "$SPEC_TABLES" == "" ]]; then
      SPEC_TABLES="$current_param"
    else
      SPEC_TABLES="${SPEC_TABLES}
${current_param}"
    fi

    shift
    counter=$(($counter + 1))
    current_param="$1"
  done


  for spec_table in $SPEC_TABLES; do
    local found=false
    for real_table in $tables; do
      if [[ "$real_table" == "$spec_table" ]]; then
        found=true
        break
      fi
    done
    
    if [[ $found == false ]]; then
      echo  -e "Specified table: $spec_table does not exist in $db!  Tables are:\n$tables"
      exit 1
    fi
  done
  echo "$SPEC_TABLES"
}


function show_usage()
{
  echo "mdber.sh <mode> <database> [table1, table2, ...]"
  echo -e "\nModes:"
  echo "show : display info"
  echo "schema : schema dump"
  echo "data : data dump"
  echo "all : do all actions; create .info (show) .schema.sql (schema) and .data.sql (data)"
}

function get_tables()
{
  local db="$1"
  local TABLES=$(mdb-tables -1 $db)
  echo "$TABLES"
}

function count_tables()
{
  local TABLES="$1"
  local num_tables=$(echo "$TABLES" | wc -l)
  echo "$num_tables"
}

function sanitize_name()
{
  local sane=$(echo "$1" | tr " " "_")
  echo "$sane"
}

function do_show_database()
{
  local db="$1"
  local redir_to="$2"
  local db_ver=$(mdb-ver "$db")
  local tables=$(get_tables "$db")
  local num_tables=$(count_tables "$tables")
  
  if [[ "$redir_to" == "" ]]; then
    echo -e "Database \"$db\" format $db_ver\n\nTables ($num_tables):"
  else
    echo "" >$redir_to
    echo -e "Database \"$db\" format $db_ver\n\nTables ($num_tables):" >>$redir_to
  fi

  for a_table in $tables; do
    if [[ "$redir_to" == "" ]]; then
      echo "'$a_table'"
    else
      echo "'$a_table'" >>$redir_to
    fi
  done
}

function do_schema_database()
{
  local db="$1"
  local schema_opts=$(echo "$2" | xargs)
  local redir_to="$3"
  if [[ "$SPEC_TABLES" != "" ]]; then
    local tables="$SPEC_TABLES"
  else
    local tables=$(get_tables "$db")
  fi

  if [[ "$redir_to" != "" ]]; then
    echo "" >$redir_to
  fi


  for a_table in $tables; do
    table_schema=$(mdb-schema --no-indexes --no-not-null --no-relations --no-drop-table --table "$a_table" "$db" postgres | sed s/'BOOL'/'INTEGER'/)
    if [[ "$redir_to" == "" ]]; then
      echo "-- Table: '$a_table'"
      echo "$table_schema"
    else
      echo "-- Table: '$a_table'" >>$redir_to
      echo "$table_schema" >>$redir_to
    fi
  done
}

function do_data_database()
{
  local db="$1"
  local redir_to="$2"
  if [[ "$SPEC_TABLES" != "" ]]; then
    local tables="$SPEC_TABLES"
  else
    local tables=$(get_tables "$db")
  fi

  if [[ "$redir_to" != "" ]]; then
    echo "" >$redir_to
  fi

  for a_table in $tables; do
    if [[ "$redir_to" == "" ]]; then
      echo "-- Table: '$a_table'"
      mdb-export -D '%Y-%m-%d %H:%M:%S' -q \' -I postgres "$DATABASE" "$a_table"
    else
      echo "-- Table: '$a_table'" >>$redir_to
      mdb-export -D '%Y-%m-%d %H:%M:%S' -q \' -I postgres "$DATABASE" "$a_table" >>$redir_to
   fi
  done
}


if [[ "$1" != "" ]]; then
  SPEC_TABLES=$(get_spec_tables "$DATABASE" "$@")
  if [[ "$?" == 1 ]]; then
    echo "$SPEC_TABLES" # this is error; specified a table that does not exist in database
    exit 1
  fi
fi

if [[ "$MODE" == "" || "$DATABASE" == "" ]]; then
  show_usage
  exit 1
fi

if [[ "$MODE" == "show" ]]; then
  do_show_database "$DATABASE"
elif [[ "$MODE" == "schema" ]]; then
  do_schema_database "$DATABASE" "$SCHEMA_OPTIONS"
elif [[ "$MODE" == "data" ]]; then
  do_data_database "$DATABASE"
elif [[ "$MODE" == "all" ]]; then
  SANE_DB_NAME=$(sanitize_name "$DATABASE")
  
  do_show_database "$DATABASE" "$SANE_DB_NAME.info"
  do_schema_database "$DATABASE" "$SCHEMA_OPTIONS" "$SANE_DB_NAME.schema.sql"
  do_data_database "$DATABASE" "$SANE_DB_NAME.data.sql"
else
  echo "dunno..."
fi

