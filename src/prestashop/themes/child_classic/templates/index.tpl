{**
 * Copyright since 2007 PrestaShop SA and Contributors
 * PrestaShop is an International Registered Trademark & Property of PrestaShop SA
 *
 * NOTICE OF LICENSE
 *
 * This source file is subject to the Academic Free License 3.0 (AFL-3.0)
 * that is bundled with this package in the file LICENSE.md.
 * It is also available through the world-wide-web at this URL:
 * https://opensource.org/licenses/AFL-3.0
 * If you did not receive a copy of the license and are unable to
 * obtain it through the world-wide-web, please send an email
 * to license@prestashop.com so we can send you a copy immediately.
 *
 * DISCLAIMER
 *
 * Do not edit or add to this file if you wish to upgrade PrestaShop to newer
 * versions in the future. If you wish to customize PrestaShop for your
 * needs please refer to https://devdocs.prestashop.com/ for more information.
 *
 * @author    PrestaShop SA and Contributors <contact@prestashop.com>
 * @copyright Since 2007 PrestaShop SA and Contributors
 * @license   https://opensource.org/licenses/AFL-3.0 Academic Free License 3.0 (AFL-3.0)
 *}
{extends file='page.tpl'}

    {block name='page_content_container'}
      <section id="content" class="page-home">
        {block name='page_content_top'}{/block}

        {block name='page_content'}
          
          {* Wywołanie tylko banera/slidera *}
            {hook h='displayHome' mod='ps_banner'}
          {hook h='displayHome' mod='ps_imageslider'}
          
          
          {* Sekcja WYRÓŻNIONE *}
          <section class="home-section featured-section">
              <h2 class="home-section-title">WYRÓŻNIONE</h2>

              <div class="home-products-slider">
                  <div class="product-card">
                      <span class="new-badge">NOWY</span>
                      <a href="{$link->getProductLink(64)}">
                          <img src="{$link->getImageLink('product', '64', 'home_default')}" alt="KFD Deser piankowy">
                      </a>
                      <h3><a href="{$link->getProductLink(64)}">KFD Deser piankowy 276 g</a></h3>
                      <div class="product-prices">
                          <span class="price">19,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(64)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <span class="new-badge">NOWY</span>
                      <a href="{$link->getProductLink(63)}">
                          <img src="{$link->getImageLink('product', '63', 'home_default')}" alt="KFD Premium AAKG">
                      </a>
                      <h3><a href="{$link->getProductLink(63)}">KFD Premium AAKG - 300 g</a></h3>
                      <div class="product-prices">
                          <span class="price">42,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(63)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <span class="discount-badge">-16,36%</span>
                      <a href="{$link->getProductLink(61)}">
                          <img src="{$link->getImageLink('product', '61', 'home_default')}" alt="KFD Potassium">
                      </a>
                      <h3><a href="{$link->getProductLink(61)}">KFD Potassium - 120 tabletek</a></h3>
                      <div class="product-prices">
                          <span class="regular-price">35,00 zł</span>
                          <span class="price">21,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(61)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <span class="new-badge">NOWY</span>
                      <a href="{$link->getProductLink(57)}">
                          <img src="{$link->getImageLink('product', '57', 'home_default')}" alt="KFD Coenzyme Q10">
                      </a>
                      <h3><a href="{$link->getProductLink(57)}">KFD Coenzyme Q10 - 100 kaps.</a></h3>
                      <div class="product-prices">
                          <span class="price">34,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(57)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <span class="discount-badge">-70%</span>
                      <a href="{$link->getProductLink(56)}">
                          <img src="{$link->getImageLink('product', '56', 'home_default')}" alt="KFD Szybki Obiadek">
                      </a>
                      <h3><a href="{$link->getProductLink(56)}">KFD Szybki Obiadek - Kurczak z kaszą</a></h3>
                      <div class="product-prices">
                          <span class="regular-price">49,99 zł</span>
                          <span class="price">14,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(56)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <span class="discount-badge">-35%</span>
                      <a href="{$link->getProductLink(54)}">
                          <img src="{$link->getImageLink('product', '54', 'home_default')}" alt="KFD Vitamin D3+K2">
                      </a>
                      <h3><a href="{$link->getProductLink(54)}">KFD Vitamin D3+K2 - 200 kapsułek</a></h3>
                      <div class="product-prices">
                          <span class="regular-price">33,83 zł</span>
                          <span class="price">21,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(54)}">Szybki podgląd</a>
                  </div>
              </div>
          </section>

          {* Sekcja BIAŁKO *}
          <section class="home-section protein-section">
              <h2 class="home-section-title">BIAŁKO</h2>

              <div class="home-products-slider">
                  <div class="product-card">
                      <a href="{$link->getProductLink(51)}">
                          <img src="{$link->getImageLink('product', '51', 'home_default')}" alt="KFD Clear Whey 90">
                      </a>
                      <h3><a href="{$link->getProductLink(51)}">KFD Clear Whey 90 - 420 g</a></h3>
                      <div class="product-prices">
                          <span class="price">69,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(51)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(60)}">
                          <img src="{$link->getImageLink('product', '60', 'home_default')}" alt="KFD Shaker 700ml">
                      </a>
                      <h3><a href="{$link->getProductLink(60)}">KFD Shaker 700ml, czarny</a></h3>
                      <div class="product-prices">
                          <span class="price">10,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(60)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(55)}">
                          <img src="{$link->getImageLink('product', '55', 'home_default')}" alt="KFD Premium EAA">
                      </a>
                      <h3><a href="{$link->getProductLink(55)}">KFD Premium EAA - 375 g</a></h3>
                      <div class="product-prices">
                          <span class="price">40,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(55)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(52)}">
                          <img src="{$link->getImageLink('product', '52', 'home_default')}" alt="KFD Shaker">
                      </a>
                      <h3><a href="{$link->getProductLink(52)}">KFD Shaker 700ml bezbarwny</a></h3>
                      <div class="product-prices">
                          <span class="price">11,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(52)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(64)}">
                          <img src="{$link->getImageLink('product', '64', 'home_default')}" alt="KFD Deser">
                      </a>
                      <h3><a href="{$link->getProductLink(64)}">KFD Deser piankowy 276 g</a></h3>
                      <div class="product-prices">
                          <span class="price">19,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(64)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(59)}">
                          <img src="{$link->getImageLink('product', '59', 'home_default')}" alt="KFD Shaker PRO">
                      </a>
                      <h3><a href="{$link->getProductLink(59)}">KFD Shaker PRO 700ml</a></h3>
                      <div class="product-prices">
                          <span class="price">10,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(59)}">Szybki podgląd</a>
                  </div>
              </div>
          </section>

          {* Sekcja KREATYNA *}
          <section class="home-section creatine-section">
              <h2 class="home-section-title">KREATYNA</h2>

              <div class="home-products-slider">
                  <div class="product-card">
                      <a href="{$link->getProductLink(63)}">
                          <img src="{$link->getImageLink('product', '63', 'home_default')}" alt="KFD Premium AAKG">
                      </a>
                      <h3><a href="{$link->getProductLink(63)}">KFD Premium AAKG - 300 g</a></h3>
                      <div class="product-prices">
                          <span class="price">42,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(63)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(58)}">
                          <img src="{$link->getImageLink('product', '58', 'home_default')}" alt="KFD Premium Sauce">
                      </a>
                      <h3><a href="{$link->getProductLink(58)}">KFD Premium Sauce XXL - 800 g</a></h3>
                      <div class="product-prices">
                          <span class="price">19,49 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(58)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(57)}">
                          <img src="{$link->getImageLink('product', '57', 'home_default')}" alt="KFD Coenzyme Q10">
                      </a>
                      <h3><a href="{$link->getProductLink(57)}">KFD Coenzyme Q10 - 100 kaps.</a></h3>
                      <div class="product-prices">
                          <span class="price">34,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(57)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(61)}">
                          <img src="{$link->getImageLink('product', '61', 'home_default')}" alt="KFD Potassium">
                      </a>
                      <h3><a href="{$link->getProductLink(61)}">KFD Potassium - 120 tabletek</a></h3>
                      <div class="product-prices">
                          <span class="price">21,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(61)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(50)}">
                          <img src="{$link->getImageLink('product', '50', 'home_default')}" alt="KFD Przyprawa">
                      </a>
                      <h3><a href="{$link->getProductLink(50)}">KFD Przyprawa do sałatek 150 g</a></h3>
                      <div class="product-prices">
                          <span class="price">8,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(50)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(53)}">
                          <img src="{$link->getImageLink('product', '53', 'home_default')}" alt="Pill box">
                      </a>
                      <h3><a href="{$link->getProductLink(53)}">Pill box - pudełko na tabletki</a></h3>
                      <div class="product-prices">
                          <span class="price">3,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(53)}">Szybki podgląd</a>
                  </div>
              </div>
          </section>

          {* Sekcja ZDROWIE I KONDYCJA *}
          <section class="home-section health-section">
              <h2 class="home-section-title">ZDROWIE I KONDYCJA</h2>

              <div class="home-products-slider">
                  <div class="product-card">
                      <a href="{$link->getProductLink(57)}">
                          <img src="{$link->getImageLink('product', '57', 'home_default')}" alt="KFD Coenzyme Q10">
                      </a>
                      <h3><a href="{$link->getProductLink(57)}">KFD Coenzyme Q10 - 100 kaps.</a></h3>
                      <div class="product-prices">
                          <span class="price">34,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(57)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(54)}">
                          <img src="{$link->getImageLink('product', '54', 'home_default')}" alt="KFD Vitamin D3+K2">
                      </a>
                      <h3><a href="{$link->getProductLink(54)}">KFD Vitamin D3+K2 - 200 kapsułek</a></h3>
                      <div class="product-prices">
                          <span class="price">21,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(54)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(61)}">
                          <img src="{$link->getImageLink('product', '61', 'home_default')}" alt="KFD Potassium">
                      </a>
                      <h3><a href="{$link->getProductLink(61)}">KFD Potassium - 120 tabletek</a></h3>
                      <div class="product-prices">
                          <span class="price">21,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(61)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(55)}">
                          <img src="{$link->getImageLink('product', '55', 'home_default')}" alt="KFD Premium EAA">
                      </a>
                      <h3><a href="{$link->getProductLink(55)}">KFD Premium EAA - 375 g</a></h3>
                      <div class="product-prices">
                          <span class="price">40,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(55)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(63)}">
                          <img src="{$link->getImageLink('product', '63', 'home_default')}" alt="KFD Premium AAKG">
                      </a>
                      <h3><a href="{$link->getProductLink(63)}">KFD Premium AAKG - 300 g</a></h3>
                      <div class="product-prices">
                          <span class="price">42,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(63)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(8)}">
                          <img src="{$link->getImageLink('product', '15', 'home_default')}" alt="KFD Electrolytes">
                      </a>
                      <h3><a href="{$link->getProductLink(8)}">KFD Electrolytes - 24 tabl.</a></h3>
                      <div class="product-prices">
                          <span class="price">7,77 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(8)}">Szybki podgląd</a>
                  </div>
              </div>
          </section>

          {* Sekcja ZDROWA ŻYWNOŚĆ *}
          <section class="home-section healthy-food-section">
              <h2 class="home-section-title">ZDROWA ŻYWNOŚĆ</h2>

              <div class="home-products-slider">
                  <div class="product-card">
                      <a href="{$link->getProductLink(56)}">
                          <img src="{$link->getImageLink('product', '56', 'home_default')}" alt="KFD Szybki Obiadek">
                      </a>
                      <h3><a href="{$link->getProductLink(56)}">KFD Szybki Obiadek - Kurczak z kaszą</a></h3>
                      <div class="product-prices">
                          <span class="price">14,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(56)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(58)}">
                          <img src="{$link->getImageLink('product', '58', 'home_default')}" alt="KFD Premium Sauce">
                      </a>
                      <h3><a href="{$link->getProductLink(58)}">KFD Premium Sauce XXL - 800 g</a></h3>
                      <div class="product-prices">
                          <span class="price">19,49 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(58)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(50)}">
                          <img src="{$link->getImageLink('product', '50', 'home_default')}" alt="KFD Przyprawa">
                      </a>
                      <h3><a href="{$link->getProductLink(50)}">KFD Przyprawa do sałatek 150 g</a></h3>
                      <div class="product-prices">
                          <span class="price">8,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(50)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(64)}">
                          <img src="{$link->getImageLink('product', '64', 'home_default')}" alt="KFD Deser piankowy">
                      </a>
                      <h3><a href="{$link->getProductLink(64)}">KFD Deser piankowy 276 g</a></h3>
                      <div class="product-prices">
                          <span class="price">19,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(64)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(51)}">
                          <img src="{$link->getImageLink('product', '51', 'home_default')}" alt="KFD Clear Whey 90">
                      </a>
                      <h3><a href="{$link->getProductLink(51)}">KFD Clear Whey 90 - 420 g</a></h3>
                      <div class="product-prices">
                          <span class="price">69,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(51)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(55)}">
                          <img src="{$link->getImageLink('product', '55', 'home_default')}" alt="KFD Premium EAA">
                      </a>
                      <h3><a href="{$link->getProductLink(55)}">KFD Premium EAA - 375 g</a></h3>
                      <div class="product-prices">
                          <span class="price">40,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(55)}">Szybki podgląd</a>
                  </div>
              </div>
          </section>

          {* Sekcja NOWOŚCI *}
          <section class="home-section new-products-section">
              <h2 class="home-section-title">NOWOŚCI</h2>

              <div class="home-products-slider">
                  <div class="product-card">
                      <span class="new-badge">NOWY</span>
                      <a href="{$link->getProductLink(64)}">
                          <img src="{$link->getImageLink('product', '64', 'home_default')}" alt="KFD Deser piankowy">
                      </a>
                      <h3><a href="{$link->getProductLink(64)}">KFD Deser piankowy 276 g</a></h3>
                      <div class="product-prices">
                          <span class="price">19,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(64)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <span class="new-badge">NOWY</span>
                      <a href="{$link->getProductLink(63)}">
                          <img src="{$link->getImageLink('product', '63', 'home_default')}" alt="KFD Premium AAKG">
                      </a>
                      <h3><a href="{$link->getProductLink(63)}">KFD Premium AAKG - 300 g</a></h3>
                      <div class="product-prices">
                          <span class="price">42,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(63)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <span class="new-badge">NOWY</span>
                      <a href="{$link->getProductLink(62)}">
                          <img src="{$link->getImageLink('product', '62', 'home_default')}" alt="Fake Fizjo koszulka">
                      </a>
                      <h3><a href="{$link->getProductLink(62)}">Fake Fizjo - koszulka biała</a></h3>
                      <div class="product-prices">
                          <span class="price">100,00 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(62)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <span class="new-badge">NOWY</span>
                      <a href="{$link->getProductLink(60)}">
                          <img src="{$link->getImageLink('product', '60', 'home_default')}" alt="KFD Shaker 700ml">
                      </a>
                      <h3><a href="{$link->getProductLink(60)}">KFD Shaker 700ml, czarny</a></h3>
                      <div class="product-prices">
                          <span class="price">10,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(60)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <span class="new-badge">NOWY</span>
                      <a href="{$link->getProductLink(59)}">
                          <img src="{$link->getImageLink('product', '59', 'home_default')}" alt="KFD Shaker PRO">
                      </a>
                      <h3><a href="{$link->getProductLink(59)}">KFD Shaker PRO 700ml</a></h3>
                      <div class="product-prices">
                          <span class="price">10,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(59)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <span class="new-badge">NOWY</span>
                      <a href="{$link->getProductLink(57)}">
                          <img src="{$link->getImageLink('product', '57', 'home_default')}" alt="KFD Coenzyme Q10">
                      </a>
                      <h3><a href="{$link->getProductLink(57)}">KFD Coenzyme Q10 - 100 kaps.</a></h3>
                      <div class="product-prices">
                          <span class="price">34,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(57)}">Szybki podgląd</a>
                  </div>
              </div>
          </section>

          {* Niestandardowy blok tekstowy na końcu *}
          {hook h='displayHome' mod='ps_customtext'}

        {/block}
      </section>
    {/block}
