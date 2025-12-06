{block name='header_banner'}
  <div class="header-banner">
    {hook h='displayBanner'}
  </div>
{/block}
{block name='header_nav'}
  <nav class="header-nav">
    <div class="container">
      <div class="row hidden-sm-down" style="display: flex; align-items: center; justify-content: space-between;">

        <!-- Logo -->
        <div id="_desktop_logo">
          {if $shop.logo_details}
            {if $page.page_name == 'index'}
              <h1>{renderLogo}</h1>
            {else}
              {renderLogo}
            {/if}
          {/if}
        </div>

        <!-- Pasek wyszukiwania -->
        <div id="desktop_searchbar" style="flex: 1; ">
          <input type="text" 
                 name="s" 
                 value="" 
                 placeholder="Czego szukasz?" 
                 class="ui-autocomplete-input form-control" 
                 autocomplete="off">
                     
        <span class="search-icon">
            <i class="material-icons">&#xE8B6;</i> <!-- lupa -->
        </span>
        </div>

        <!-- Hook logowanie i koszyk -->
        <div class="header-right" style="display: flex; gap: 15px; align-items: center;">
          {hook h='displayNav1'}
          {hook h='displayNav2'}
        </div>

      </div>

      <!-- Mobile -->
      <div class="row hidden-md-up text-sm-center mobile">
        <div class="float-xs-left" id="menu-icon">
          <i class="material-icons d-inline">&#xE5D2;</i>
        </div>
        <div class="float-xs-right" id="_mobile_cart"></div>
        <div class="float-xs-right" id="_mobile_user_info"></div>
        <div class="top-logo" id="_mobile_logo"></div>
        <div class="clearfix"></div>
      </div>
    </div>
  </nav>
{/block}


{block name='header_top'}

  <div class="header-top">
    

    <div class="container">
      <div class="row">
        <div class="header-top-right col-md-12 col-sm-12 position-static">
          {hook h='displayTop'}
        </div>
      </div>

      <div id="mobile_top_menu_wrapper" class="row hidden-md-up" style="display:none;">
        <div class="js-top-menu mobile" id="_mobile_top_menu"></div>
        <div class="js-top-menu-bottom">
          <div id="_mobile_currency_selector"></div>
          <div id="_mobile_language_selector"></div>
          <div id="_mobile_contact_link"></div>
        </div>
      </div>
    </div>
  </div>
  {hook h='displayNavFullWidth'}
{/block}
