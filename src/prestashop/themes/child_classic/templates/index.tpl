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
                      <a href="{$link->getProductLink(275)}">
                          <img src="{$link->getImageLink('product', '157', 'home_default')}" alt="KFD Deser piankowy">
                      </a>
                      <h3><a href="{$link->getProductLink(275)}">KFD Nocto Blue Rebel 100 ml</a></h3>
                      <div class="product-prices">
                          <span class="price">99,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(275)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                   <span class="new-badge">NOWY</span>
                      <a href="{$link->getProductLink(11)}">
                          <img src="{$link->getImageLink('product', '11', 'home_default')}" alt="KFD Magnesium+">
                      </a>
                      <h3><a href="{$link->getProductLink(11)}">KFD Magnesium+ - 24 tabletki musujące</a></h3>
                      <div class="product-prices">
                          <span class="price">7,77 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(11)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                   <span class="discount-badge">-16,95%</span>
                      <a href="{$link->getProductLink(8)}">
                          <img src="{$link->getImageLink('product', '9', 'home_default')}" alt="KFD Premium Creatine">
                      </a>
                      <h3><a href="{$link->getProductLink(8)}">KFD Premium Creatine - 500 g</a></h3>
                      <div class="product-prices">
                          <span class="regular-price">35,99 zł</span>
                          <span class="price">29,89 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(8)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                   <span class="new-badge">NOWY</span>
                      <a href="{$link->getProductLink(10)}">
                          <img src="{$link->getImageLink('product', '635', 'home_default')}" alt="KFD Multivitamin & Minerals">
                      </a>
                      <h3><a href="{$link->getProductLink(10)}">KFD Multivitamin & Minerals - 24 tabletki musujące</a></h3>
                      <div class="product-prices">
                          <span class="price">7,97 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(10)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(70)}">
                          <img src="{$link->getImageLink('product', '694', 'home_default')}" alt="KFD Kisiel">
                      </a>
                      <h3><a href="{$link->getProductLink(70)}">KFD Delicates Kisiel na zimno 259 g</a></h3>
                      <div class="product-prices">
                          <span class="price">19,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(70)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(43)}">
                          <img src="{$link->getImageLink('product', '668', 'home_default')}" alt="KFD Premium Citrulline">
                      </a>
                      <h3><a href="{$link->getProductLink(43)}">KFD Premium Citrulline - 400 g</a></h3>
                      <div class="product-prices">
                          <span class="price">49,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(43)}">Szybki podgląd</a>
                  </div>
              </div>
          </section>

          {* Sekcja BIAŁKO *}
          <section class="home-section protein-section">
              <h2 class="home-section-title"><a href="https://localhost:8443/index.php?id_category=16&controller=category">BIAŁKO</a></h2>

              <div class="home-products-slider">
               

               

                  <div class="product-card">
                      <a href="{$link->getProductLink(12)}">
                          <img src="{$link->getImageLink('product', '637', 'home_default')}" alt="KFD Premium WPC 82 XXL">
                      </a>
                      <h3><a href="{$link->getProductLink(12)}">KFD Premium WPC 82 XXL - 900 g</a></h3>
                      <div class="product-prices">
                          <span class="price">77,77 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(12)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(7)}">
                          <img src="{$link->getImageLink('product', '8', 'home_default')}" alt="KFD Pure WPC 82 Instant">
                      </a>
                      <h3><a href="{$link->getProductLink(7)}">KFD Pure WPC 82 Instant - 700 g</a></h3>
                      <div class="product-prices">
                          <span class="price">55,55 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(7)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(20)}">
                          <img src="{$link->getImageLink('product', '17', 'home_default')}" alt="KFD REGULAR WPC 80">
                      </a>
                      <h3><a href="{$link->getProductLink(20)}">KFD REGULAR WPC 80 - 750 g</a></h3>
                      <div class="product-prices">
                          <span class="price">62,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(20)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(32)}">
                          <img src="{$link->getImageLink('product', '27', 'home_default')}" alt="KFD Premium WPI 90">
                      </a>
                      <h3><a href="{$link->getProductLink(32)}">KFD Premium WPI 90 - 700 g</a></h3>
                      <div class="product-prices">
                          <span class="price">119,99zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(32)}">Szybki podgląd</a>
                  </div>

                    <div class="product-card">
                      <a href="{$link->getProductLink(24)}">
                          <img src="{$link->getImageLink('product', '21', 'home_default')}" alt="KFD Premium WPC 82">
                      </a>
                      <h3><a href="{$link->getProductLink(24)}">KFD Premium WPC 82 - 700 g</a></h3>
                      <div class="product-prices">
                          <span class="price">66,66 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(24)}">Szybki podgląd</a>
                  </div> 
                  
                  <div class="product-card">
                      <a href="{$link->getProductLink(46)}">
                          <img src="{$link->getImageLink('product', '671', 'home_default')}" alt="KFD Premium X-Whey">
                      </a>
                      <h3><a href="{$link->getProductLink(46)}">KFD Premium X-Whey - 540 g</a></h3>
                      <div class="product-prices">
                          <span class="price">66,66 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(46)}">Szybki podgląd</a>
                  </div>
              </div>
          </section>

          {* Sekcja KREATYNA *}
          <section class="home-section creatine-section">
              <h2 class="home-section-title"><a href="https://localhost:8443/index.php?id_category=14&controller=category">KREATYNA</a></h2>

              <div class="home-products-slider">
                 

                    <div class="product-card">
                   <span class="discount-badge">-16,95%</span>
                      <a href="{$link->getProductLink(8)}">
                          <img src="{$link->getImageLink('product', '9', 'home_default')}" alt="KFD Premium Creatine">
                      </a>
                      <h3><a href="{$link->getProductLink(8)}">KFD Premium Creatine - 500 g</a></h3>
                      <div class="product-prices">
                          <span class="regular-price">35,99 zł</span>
                          <span class="price">29,89 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(8)}">Szybki podgląd</a>
                  </div>


                  <div class="product-card">
                      <a href="{$link->getProductLink(23)}">
                          <img src="{$link->getImageLink('product', '20', 'home_default')}" alt="KFD Premium Creatine 250g">
                      </a>
                      <h3><a href="{$link->getProductLink(23)}">KFD Premium Creatine - 250 g</a></h3>
                      <div class="product-prices">
                          <span class="price">22,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(23)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(545)}">
                          <img src="{$link->getImageLink('product', '1161', 'home_default')}" alt="Megabol Creatine Alkaline">
                      </a>
                      <h3><a href="{$link->getProductLink(545)}">Megabol Creatine Alkaline 1500 120 kap.</a></h3>
                      <div class="product-prices">
                          <span class="price">38,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(545)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(960)}">
                          <img src="{$link->getImageLink('product', '538', 'home_default')}" alt="7 Nutrition Creatine HCL">
                      </a>
                      <h3><a href="{$link->getProductLink(960)}">7 Nutrition Creatine HCL 350g</a></h3>
                      <div class="product-prices">
                          <span class="price">98,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(960)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(253)}">
                          <img src="{$link->getImageLink('product', '877', 'home_default')}" alt="Olimp Creatine Mega Caps">
                      </a>
                      <h3><a href="{$link->getProductLink(253)}">Olimp Creatine Mega Caps - 400 kaps.</a></h3>
                      <div class="product-prices">
                          <span class="price">129,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(253)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(649)}">
                          <img src="{$link->getImageLink('product', '1265', 'home_default')}" alt="Bio Tech Mega Creatine">
                      </a>
                      <h3><a href="{$link->getProductLink(649)}">Bio Tech Mega Creatine - 120 kaps.</a></h3>
                      <div class="product-prices">
                          <span class="price">58,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(649)}">Szybki podgląd</a>
                  </div>
              </div>
          </section>

          {* Sekcja ZDROWIE I KONDYCJA *}
          <section class="home-section health-section">
              <h2 class="home-section-title"><a href="https://localhost:8443/index.php?id_category=4&controller=category">ZDROWIE I KONDYCJA</a></h2>

              <div class="home-products-slider">
                

                  <div class="product-card">
                      <a href="{$link->getProductLink(6)}">
                          <img src="{$link->getImageLink('product', '631', 'home_default')}" alt="KFD Vitapak+">
                      </a>
                      <h3><a href="{$link->getProductLink(6)}">KFD Vitapak+ 90 tabl.</a></h3>
                      <div class="product-prices">
                          <span class="price">25,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(6)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(594)}">
                          <img src="{$link->getImageLink('product', '321', 'home_default')}" alt="ActivLab Caffeine Power">
                      </a>
                      <h3><a href="{$link->getProductLink(594)}">ActivLab Caffeine Power - 60 kaps.</a></h3>
                      <div class="product-prices">
                          <span class="price">19,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(594)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(428)}">
                          <img src="{$link->getImageLink('product', '1048', 'home_default')}" alt="Trec Caffeine 200 Plus">
                      </a>
                      <h3><a href="{$link->getProductLink(428)}">Trec Caffeine 200 Plus 60 caps.</a></h3>
                      <div class="product-prices">
                          <span class="price">24,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(428)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(218)}">
                          <img src="{$link->getImageLink('product', '129', 'home_default')}" alt="KFD Pure Caffeine">
                      </a>
                      <h3><a href="{$link->getProductLink(218)}">KFD Pure Caffeine - 200 g</a></h3>
                      <div class="product-prices">
                          <span class="price">39,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(218)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(650)}">
                          <img src="{$link->getImageLink('product', '350', 'home_default')}" alt="OLIMP Caffeine Kick">
                      </a>
                      <h3><a href="{$link->getProductLink(650)}">OLIMP Caffeine Kick 200 mg - 60 kaps.</a></h3>
                      <div class="product-prices">
                          <span class="price">21,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(650)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(16)}">
                          <img src="{$link->getImageLink('product', '641', 'home_default')}" alt="KFD ZMB Comfort">
                      </a>
                      <h3><a href="{$link->getProductLink(16)}">KFD ZMB Comfort - 135 tabletek</a></h3>
                      <div class="product-prices">
                          <span class="price">19,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(16)}">Szybki podgląd</a>
                  </div>
              </div>
          </section>

          {* Sekcja ZDROWA ŻYWNOŚĆ *}
          <section class="home-section healthy-food-section">
              <h2 class="home-section-title"><a href="https://localhost:8443/index.php?id_category=18&controller=category">ZDROWA ŻYWNOŚĆ</a></h2>

              <div class="home-products-slider">
                  
                  <div class="product-card">
                      <a href="{$link->getProductLink(17)}">
                          <img src="{$link->getImageLink('product', '642', 'home_default')}" alt="KFD Erytrytol">
                      </a>
                      <h3><a href="{$link->getProductLink(17)}">KFD Erytrytol 1000 g</a></h3>
                      <div class="product-prices">
                          <span class="price">24,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(17)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(325)}">
                          <img src="{$link->getImageLink('product', '178', 'home_default')}" alt="KFD Pulchny Pankejk">
                      </a>
                      <h3><a href="{$link->getProductLink(325)}">KFD Pulchny Pankejk Proteinowy 900 g</a></h3>
                      <div class="product-prices">
                          <span class="price">43,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(325)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(254)}">
                          <img src="{$link->getImageLink('product', '878', 'home_default')}" alt="KFD Fit Mleczna Czekolada">
                      </a>
                      <h3><a href="{$link->getProductLink(254)}">KFD Fit Mleczna Czekolada 100 g</a></h3>
                      <div class="product-prices">
                          <span class="price">12,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(254)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(175)}">
                          <img src="{$link->getImageLink('product', '799', 'home_default')}" alt="KFD Delicates Hazelnut">
                      </a>
                      <h3><a href="{$link->getProductLink(175)}">KFD Delicates Hazelnut & Milk 500 g</a></h3>
                      <div class="product-prices">
                          <span class="price">24,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(175)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(71)}">
                          <img src="{$link->getImageLink('product', '51', 'home_default')}" alt="KFD Szybki Obiadek">
                      </a>
                      <h3><a href="{$link->getProductLink(71)}">KFD Szybki Obiadek - Kurczak z makaronem</a></h3>
                      <div class="product-prices">
                          <span class="price">14,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(71)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <a href="{$link->getProductLink(76)}">
                          <img src="{$link->getImageLink('product', '53', 'home_default')}" alt="KFD Premium Sauce Karmelowy">
                      </a>
                      <h3><a href="{$link->getProductLink(76)}">KFD Premium Sauce - Karmelowy 410 g</a></h3>
                      <div class="product-prices">
                          <span class="price">11,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(76)}">Szybki podgląd</a>
                  </div>
              </div>
          </section>

          {* Sekcja NOWOŚCI *}
          <section class="home-section new-products-section">
              <h2 class="home-section-title">NOWOŚCI</h2>

              <div class="home-products-slider">
                  <div class="product-card">
                      <span class="new-badge">NOWY</span>
                      <a href="{$link->getProductLink(492)}">
                          <img src="{$link->getImageLink('product', '277', 'home_default')}" alt="feel FIT Ciastka DUO">
                      </a>
                      <h3><a href="{$link->getProductLink(492)}">feel FIT Ciastka DUO Sugar Free - 176 g</a></h3>
                      <div class="product-prices">
                          <span class="price">12,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(492)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <span class="new-badge">NOWY</span>
                      <a href="{$link->getProductLink(370)}">
                          <img src="{$link->getImageLink('product', '208', 'home_default')}" alt="feel FIT Ciastka ENJOY">
                      </a>
                      <h3><a href="{$link->getProductLink(370)}">feel FIT Ciastka ENJOY! 96 - 100 g</a></h3>
                      <div class="product-prices">
                          <span class="price">9,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(370)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <span class="new-badge">NOWY</span>
                      <a href="{$link->getProductLink(81)}">
                          <img src="{$link->getImageLink('product', '56', 'home_default')}" alt="KFD Shaker różowy">
                      </a>
                      <h3><a href="{$link->getProductLink(81)}">KFD Shaker 700 ml, różowy - You can do it</a></h3>
                      <div class="product-prices">
                          <span class="price">10,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(81)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <span class="new-badge">NOWY</span>
                      <a href="{$link->getProductLink(95)}">
                          <img src="{$link->getImageLink('product', '719', 'home_default')}" alt="KFD Caffeine">
                      </a>
                      <h3><a href="{$link->getProductLink(95)}">KFD Caffeine - 100 kapsułek (200 mg)</a></h3>
                      <div class="product-prices">
                          <span class="price">15,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(95)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <span class="new-badge">NOWY</span>
                      <a href="{$link->getProductLink(284)}">
                          <img src="{$link->getImageLink('product', '162', 'home_default')}" alt="Ostrovit Flavour Drops">
                      </a>
                      <h3><a href="{$link->getProductLink(284)}">Ostrovit Flavour Drops - 30 ml</a></h3>
                      <div class="product-prices">
                          <span class="price">8,99 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(284)}">Szybki podgląd</a>
                  </div>

                  <div class="product-card">
                      <span class="new-badge">NOWY</span>
                      <a href="{$link->getProductLink(849)}">
                          <img src="{$link->getImageLink('product', '1459', 'home_default')}" alt="Bio Tech USA Vitamin D3">
                      </a>
                      <h3><a href="{$link->getProductLink(849)}">Bio Tech USA Vitamin D3 - 60 kaps.</a></h3>
                      <div class="product-prices">
                          <span class="price">31,90 zł</span>
                      </div>
                      <a class="quick-view" href="{$link->getProductLink(849)}">Szybki podgląd</a>
                  </div>
              </div>
          </section>

          {* Niestandardowy blok tekstowy na końcu *}
          {hook h='displayHome' mod='ps_customtext'}

        {/block}
      </section>
    {/block}
