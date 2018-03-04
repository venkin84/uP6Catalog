//var categoriesHTML = [];
//for (var i = 0; i < categories.length; i++) {
//	categoriesHTML.push(categories[i].name + '<br>');
//}
//
//$("#cat").html(categoriesHTML.join(""));

$("#tree").delegate("li", "click", function(event) {
	$(event.target);
});

//$("#tree").click(function(event){
//	$(event.target).toggleClass("focused");
//});

$("document").ready(function(){
	$( "#tree" ).children().find( "li" ).has( "ul" ).find("span").first().removeClass( "invisible" );
	$( "#tree" ).children().find( "li" ).has( "ul" ).find("span").first().addClass( "visible" );
});