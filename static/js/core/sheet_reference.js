SheetReferenceJs = {
    x: 0
    , y:0
    , height: 0
    , width: 0
    , color: ''
    , create: function(data) {
        var ref = jQuery.extend({}, SheetReferenceJs);
        ref.x = data.x;
        ref.y = data.y;
        ref.height = data.height;
        ref.width = data.width;
        ref.color = data.color;

        return ref;
    }
    , toJson: function () {
        return {
            x: this.x
            , y: this.y
            , height: this.height
            , width: this.width
            , color: this.color
        }
    }
    , toString: function () {
        return JSON.stringify(this.toJson())
    }
    , isEqualColor: function (color) {
        return this.color === color
    }
    , inBounds: function (start, distance, start_ref, distance_ref) {
        return (
            this.between(start, start_ref, (start_ref+(distance_ref)), true)
            &&
            this.between((start+distance), start_ref, (start_ref+(distance_ref)), true)
        );

    }
    , between: function (value, a, b, inclusive) {
        var min = Math.min.apply(Math, [a,b]);
        var max = Math.max.apply(Math, [a,b]);

        return inclusive ? ((value >= min) && (value <= max)) : ((value > min) && (value < max));
    }
    , withinBounds: function (sheet_reference_js) {
    //alert(sheet_reference_js.y, sheet_reference_js.height, this.y, this.height)
        return (
            this.isEqualColor(sheet_reference_js.color)
            &&
            this.inBounds(sheet_reference_js.y, sheet_reference_js.height, this.y, this.height)
            &&
            this.inBounds(sheet_reference_js.x, sheet_reference_js.width, this.x, this.width)
        );
    }
}
