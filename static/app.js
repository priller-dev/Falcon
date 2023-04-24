function make_visible() {
    document.querySelector('#hide').classList.remove('col-md-7');
    document.querySelector('#hide').classList.remove('d-flex');
    document.querySelector('#hide').classList.remove('flex-center');
    document.querySelector('#hidden').style.display = 'block';
}
function submitForm(event) {
    event.preventDefault();
}
$(document).ready(function(){
    $('#submit').on('click', function(){
        $email = $('#email').val();
        document.querySelector('#tex').innerHTML = $email;

        if($email === ""){
            alert("Please complete field");
        }else{
            $.ajax({
                type: "POST",
                url: "forgot",
                data:{
                    email: $email,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(){
                    // alert('Save Data');
                    $('#email').val('');
                    window.location = "/auth/login";
                }
            });
        }
    });
});