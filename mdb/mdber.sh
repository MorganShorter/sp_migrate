#!/bin/bash
MODE="$1"
DATABASE="$2"
#Internal Field Seperator - so we can iterate through space containing table names
IFS=$'\012'

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
  local redir_to="$2"
  local tables=$(get_tables "$db")

  if [[ "$redir_to" != "" ]]; then
    echo "" >$redir_to
  fi

  for a_table in $tables; do
    table_schema=$(mdb-schema --no-indexes --no-not-null --no-relations --table "$a_table" "$db" postgres | sed s/'BOOL'/'INTEGER'/)
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
  local tables=$(get_tables "$db")

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

if [[ "$MODE" == "" || "$DATABASE" == "" ]]; then
  show_usage
  exit 1
fi

if [[ "$MODE" == "show" ]]; then
  do_show_database "$DATABASE"
elif [[ "$MODE" == "schema" ]]; then
  do_schema_database "$DATABASE"
elif [[ "$MODE" == "data" ]]; then
  do_data_database "$DATABASE"
elif [[ "$MODE" == "all" ]]; then
  SANE_DB_NAME=$(sanitize_name "$DATABASE")
  
  do_show_database "$DATABASE" "$SANE_DB_NAME.info"
  do_schema_database "$DATABASE" "$SANE_DB_NAME.schema.sql"
  do_data_database "$DATABASE" "$SANE_DB_NAME.data.sql"
else
  echo "dunno..."
fi

