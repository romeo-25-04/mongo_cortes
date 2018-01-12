$('.material_have').on('propertychange input', function (e) {
    var valueChanged = false;
    var this_id = e.target.id;

    if (e.type=='propertychange') {
        valueChanged = e.originalEvent.propertyName=='value';
    } else {
        valueChanged = true;
    }
    if (valueChanged) {
        var this_val = $('#'+this_id).val();
        var need_val = parseInt($('#'+this_id+'_need').html());
        var diffP = need_val-this_val;
        $('#'+this_id+'_diffP').html(diffP);
        $('#'+this_id+'_diffS').html(diffP*2);
        console.log(this_id, need_val, this_val, diffP);
    }
});

$('.product_number').on('propertychange input', function (e) {
    var valueChanged = false;
    var this_id = e.target.id;

    if (e.type=='propertychange') {
        valueChanged = e.originalEvent.propertyName=='value';
    } else {
        valueChanged = true;
    }
    if (valueChanged) {
        var this_val = $('#'+this_id).val();
        var price_prod_val = $('#'+this_id+'_price').data('value');
        var price_prod = parseInt(price_prod_val);
        var receipt = this_val * price_prod;
        $('#'+this_id+'_receipt').html("$ " + Number(receipt).toLocaleString('de'));
        console.log(this_id, this_val, price_prod_val, receipt);
    }
});
