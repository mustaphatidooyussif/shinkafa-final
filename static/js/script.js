// https://bootsnipp.com/snippets/eNbOa

$(document).ready( function() {
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            
            reader.onload = function (e) {
                $('#img-upload').attr('src', e.target.result);
            }
            
            reader.readAsDataURL(input.files[0]);
        }
    }

    $("#imgInp").change(function(){
        readURL(this);
    }); 
    
    $("file").change(function() {
        document.getElementById("form").submit();
    });
});