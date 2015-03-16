TextManagerJs = {
    actions: {
        selectAll: function (element) {
            var element_name = $(element).attr('name');
            var is_checked = $(element).prop("checked")

            $('input:checkbox[name^=' + element_name + '_]').prop("checked", is_checked)
        }
        , deleteSelected: function (element) {

        }
    }
}
