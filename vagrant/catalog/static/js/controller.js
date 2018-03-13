
$("a.itemName").click(function(){
	$.ajax({
        type: 'GET',
        url: '/item/' + $(this).find("span").text() + '/view',
        success: function (result){
        		var descID = "#description" + result.id;
        		console.log($(descID).find("div").text());
            $(descID).find("div").html(result.description);
            console.log(result.description);
        }
    });
});

