require(['jquery'], function ($) {

  var teamFilter = {

    $filterDropdown: null,
    $filterDropdownBtn: null,
    $filterDropdownLabel: null,
    $filterDropdownItems: null,

    init: function () {

      var _this = teamFilter;

      _this.$filterDropdown = $('.fi-page-nav__filters');
      _this.$parentSection = _this.$filterDropdown.closest('section');
      if (_this.$parentSection.length == 0)
        _this.$parentSection = $('body');
      _this.$filterDropdownBtn = _this.$filterDropdown.find('.fi-page-nav__filters-btn');
      _this.$filterDropdownLabel = _this.$filterDropdown.find('.fi-page-nav__filters-label');
      _this.$filterDropdownItems = _this.$filterDropdown.find('a');

      _this.$filterDropdownItems.on('click', function (e) {
        e.preventDefault();

        _this.$parentSection.find('.fi-mu__link, .fi-mu').removeClass('fi-mu--filter-hidden');
        _this.$parentSection.find('.fi-mu-list').removeClass("hidden");

        var $teamID = $(this).data('team-id');

        _this.$filterDropdown.removeClass('active');
        _this.$filterDropdown.addClass('selected');
        _this.$filterDropdownBtn.find('a').remove();
        $(this).clone().insertAfter(_this.$filterDropdownLabel.hide());

        _this.$parentSection.find('.fi-mu__link, .fi-mu').each(function () {
          if ($(this).find('.fi-t[data-team-id=' + $teamID + ']').length == 0) {
            $(this).addClass('fi-mu--filter-hidden');
          }
        });

        _this.$parentSection.find('.fi-mu-list').each(function () {
          if ($(this).find('.fi-t[data-team-id=' + $teamID + ']').length == 0) {
            $(this).addClass('hidden');
          }
        });

      });

      _this.$filterDropdownBtn.on('click', function (e) {
        _this.resetSearch(e);
      });

    },

    resetSearch: function (e) {
      e.preventDefault();

      var _this = teamFilter;

      if (!$(e.target).closest('.fi-page-nav__filters-close').length > 0) {
        _this.$filterDropdown.toggleClass('active');
      } else {
        _this.$filterDropdownBtn.find('a').remove();
        _this.$filterDropdownLabel.show();
        _this.$filterDropdown.removeClass('selected');
        $('.fi-mu__link, .fi-mu').removeClass('fi-mu--filter-hidden');
        $('.fi-mu-list').removeClass("hidden");
      }
    }

  };

  $(document).ready(function () {
    teamFilter.init();
  });

});