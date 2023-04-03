$(document).ready(function() {
    $().ready(function() {
        $sidebar = $('.sidebar');
      //  $navbar = $('.navbar');
        $main_panel = $('.main-panel');

        $full_page = $('.full-page');

        //$sidebar_responsive = $('body > .navbar-collapse');
        sidebar_mini_active = false;
        white_color = true;

        window_width = $(window).width();


        $('.switch-sidebar-mini input').on("switchChange.bootstrapSwitch", function() {
            var $btn = $(this);

            if (sidebar_mini_active == true) {
                $('body').removeClass('sidebar-mini');
                sidebar_mini_active = false;
               // blackDashboard.showSidebarMessage('Sidebar mini deactivated...');
            } else {
                $('body').addClass('sidebar-mini');
                sidebar_mini_active = false;
              //  blackDashboard.showSidebarMessage('Sidebar mini activated...');
            }

            // we simulate the window Resize so the charts will get updated in realtime.
            var simulateWindowResize = setInterval(function() {
                window.dispatchEvent(new Event('resize'));
            }, 180);

            // we stop the simulation of Window Resize after the animations are completed
            setTimeout(function() {
                clearInterval(simulateWindowResize);
            }, 1000);
        });

        // set white theme
            $('body').addClass('white-content');
            localStorage.setItem("light_color", "true");
            $('.switch input').prop("checked", false);
    });
});


$(document).ready(function () {
    let light_color = localStorage.getItem("light_color");

    if (light_color === "true"||light_color==null) {
        $('body').addClass('white-content');
        $('.switch input').prop("checked", true)
    } else {
        $('.switch input').prop("checked", false)
    }


    $('.switch input').on("change", function () {
        light_color = localStorage.getItem("light_color");

        if (light_color === "false") {
            localStorage.setItem("light_color", "true");

            $('body').addClass('change-background');
            setTimeout(function () {
                $('body').removeClass('change-background');
                $('body').removeClass('white-content');
            }, 400);

        } else {
            localStorage.setItem("light_color", "false");

            $('body').addClass('change-background');
            setTimeout(function () {
                $('body').removeClass('change-background');
                $('body').addClass('white-content');
            }, 400);
        }
    });
});