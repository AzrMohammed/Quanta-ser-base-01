 $(document).ready(function () {
     // Add smooth scrolling to all links in navbar + footer link
     $(".navbar a, footer a[href='#myPage']").on('click', function (event) {
         if (this.hash !== "") {
             event.preventDefault();
             var hash = this.hash;
             $('html, body').animate({
                 scrollTop: $(hash).offset().top
             }, 900, function () {
                 window.location.hash = hash;
             });
         }
     });
     //hide nav bar
     $('.navbar-collapse a').on('click', function () {
         $('.navbar-toggle').click();
     });
     //nav active a color
     $(".navbar-nav li a").click(function () {
         $('.navbar-nav').find(".active").removeClass("active");
         $(this).parent().addClass("active");
     });
 });
