#! /usr/bin/env bash

export blue_geo_scope_help=$(python3 -c "from blue_geo.catalog.generic.generic.scope import DatacubeScope; print(DatacubeScope.help)")
export blue_geo_datacube_ingest_options="$(xtra ~copy_template,dryrun,overwrite,upload,)scope=$blue_geo_scope_help"

function blue_geo_datacube_ingest() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        options=$blue_geo_datacube_ingest_options
        abcli_show_usage "@datacube ingest$ABCUL[$options]$ABCUL[.|<datacube-id>]$ABCUL[<args>]" \
            "ingest <datacube-id>.${ABCUL2}all: ALL files.${ABCUL2}metadata (default): any < 1 MB.${ABCUL2}quick: around 200 MB, decided by the datacube class.${ABCUL2}suffix=<suffix>: any *<suffix>."
        return
    fi

    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local scope=$(abcli_option "$options" scope metadata)
    local do_overwrite=$(abcli_option_int "$options" overwrite 0)
    local do_upload=$(abcli_option_int "$options" upload 0)

    local datacube_id=$(abcli_clarify_object $2 .)

    abcli_log "🧊 ingesting $datacube_id ..."

    local template_object_name=$(blue_geo_datacube get template $datacube_id)
    local do_copy_template=1
    [[ "$template_object_name" == "unknown-template" ]] &&
        do_copy_template=0
    do_copy_template=$(abcli_option_int "$options" copy_template $do_copy_template)

    [[ "$do_copy_template" == 1 ]] &&
        abcli_clone \
            ~meta \
            $template_object_name \
            $datacube_id

    python3 -m blue_geo.datacube \
        ingest \
        --datacube_id $datacube_id \
        --dryrun $do_dryrun \
        --overwrite $do_overwrite \
        --scope $scope \
        "${@:3}"
    local status="$?"

    [[ "$do_upload" == 1 ]] &&
        abcli_upload - $datacube_id

    return $status
}
