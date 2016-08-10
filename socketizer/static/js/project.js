/**
 * Namespace: Socketizer
 * @namespace
 */
var Socketizer = Socketizer || {};

/**
 * Module: Socketizer.index
 * @description
 * @namespace
 * @memberof Socketizer.index
 */
Socketizer.index = (function () {
  // private variables

  // public variables go into public dict
  var self = {};

  self.main = function () {
    self.poolInfo();
    self.calculator();
  };

  self.poolInfo = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
      if (xhttp.readyState == 4 && xhttp.status == 200) {
        data = JSON.parse(xhttp.responseText);
        var info = document.querySelector('#poolInfo');
        info.innerHTML = "<span class='label bg-socketizer-opposite strong'><span class='blinkit'>LIVE NOW</span></span> " +
          "Domains connected: <span class='label bg-socketizer-opposite strong'>" +
          data.DomainCount + "</span> Total clients: <span class='label bg-socketizer-opposite strong'>" +
          data.ClientSub + "</span> refresh page to check again.";
      }
    };
    xhttp.open('GET', 'cmd/pool-info/', true);
    xhttp.send();
  };

  self.calculator = function () {
    $('#concurrentVisitors').on('click change keyup', function () {
      var vi = parseInt($(this).val());
      if (isNaN(vi)) {
        vi = 0
      }
      $('#users').text(vi);
      $('#price').text((1 + vi * 0.1).toFixed(2));
    });
  };

  // expose all in public
  return self;
})();

/**
 * Module: Socketizer.ui
 * @description
 * @namespace
 * @memberof Socketizer.ui
 */
Socketizer.ui = (function () {
  // private variables

  // public variables go into public dict
  var self = {};

  self.main = function () {
    self.smoothScroll();
    self.niceScroll();
    self.bootstrapJs();
    self.toTop();
  };

  self.sticky = function () {
    var stickyToggle = function (sticky, stickyWrapper, scrollElement) {
      var stickyHeight = sticky.outerHeight();
      var stickyTop = stickyWrapper.offset().top;
      if (scrollElement.scrollTop() >= stickyTop) {
        stickyWrapper.height(stickyHeight);
        sticky.addClass("is-sticky");
        sticky.removeClass("socketizer-r-b");
        sticky.addClass('socketizer-b-r');
      }
      else {
        sticky.removeClass("is-sticky");
        sticky.removeClass("socketizer-b-r");
        sticky.addClass('socketizer-r-b');
        stickyWrapper.height('auto');
      }
    };

    // Find all data-toggle="sticky-onscroll" elements
    $('[data-toggle="sticky-onscroll"]').each(function () {
      var sticky = $(this);
      var stickyWrapper = $('<div>').addClass('sticky-wrapper'); // insert hidden element to maintain actual top offset on page
      sticky.before(stickyWrapper);
      sticky.addClass('sticky');

      // Scroll & resize events
      $(window).on('scroll.sticky-onscroll resize.sticky-onscroll', function () {
        stickyToggle(sticky, stickyWrapper, $(this));
      });

      // On page load
      stickyToggle(sticky, stickyWrapper, $(window));
    });
  };

  self.bootstrapJs = function () {
    $('[data-toggle="tooltip"]').tooltip();
    $('[data-toggle="popover"]').popover();
  };

  self.smoothScroll = function () {
    $('a[href*="#"]:not([href="#"])').click(function () {
      if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
        if (target.length) {
          $('html, body').animate({
            scrollTop: target.offset().top - 60
          }, 800);
          return false;
        }
      }
    });
  };

  self.niceScroll = function () {
    $("html").niceScroll({
      scrollspeed: 60,
      mousescrollstep: 120
    });
  };

  self.toTop = function () {
    $(window).scroll(function () {
      if ($(this).scrollTop() > 700) {
        $('.toTop').fadeIn();
      } else {
        $('.toTop').fadeOut();
      }
    });

    //Click event to scroll to top
    $('.toTop').click(function () {
      $('html, body').animate({scrollTop: 0}, 800);
      return false;
    });
  };

  // expose all in public
  return self;
})();

/**
 * Module: Socketizer.base
 * @description
 * @namespace
 * @memberof Socketizer.base
 */
Socketizer.base = (function () {
  // private variables

  // public variables go into public dict
  var self = {};

  self.init = function () {
    Socketizer.ui.main();
    Socketizer.index.main();
  };

  // expose all in public
  return self;
})();
$(document).ready(function () {
  Socketizer.base.init();
});
