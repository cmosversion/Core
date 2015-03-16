TextManagerIndexJs = {
    init: function () {
        $(document).ready(function() {
            $('.definitions_header').first().css('width','88%');
        });
    }
    , actions: {
        selectAll: function (element) {
            var element_name = $(element).attr('name');
            var is_checked = $(element).prop("checked");
            var parent_table = $(element).parents('table').first()

            $(parent_table).find('input:checkbox[name^=' + element_name + '_]').prop("checked", is_checked);

        }
        , processSelected: function(element) {
            var element_name = $(element).attr('name');
            var parent_table = $(element).parents('table').first();

            var count = 0;
            var ids = [];

            $(parent_table).find('input:checked[name^=' + element_name + '_]').each(function (index, item) {
                ids[count++] = element_name + '=' + $(item).val();
            });

            if (ids.length <= 0) {
                return false;
            }

            var href = $(element).attr('href');

            ids = ids.join('&');

            href += '?' + ids;

            $(element).attr('href', href);

            return true;
        }
    }
}
TextManagerIndexJs.init();
