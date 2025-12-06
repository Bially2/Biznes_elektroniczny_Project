
<section class="contact-form">
  <form action="{$urls.pages.contact}" method="post" {if $contact.allow_file_upload}enctype="multipart/form-data"{/if}>
    {if $notifications}
      <div class="col-xs-12 alert {if $notifications.nw_error}alert-danger{else}alert-success{/if}">
        <ul>
          {foreach $notifications.messages as $notif}
            <li>{$notif}</li>
          {/foreach}
        </ul>
      </div>
    {/if}

    {if !$notifications || $notifications.nw_error}
      <section class="form-fields">

        <div class="form-group row">
          <div class="col-md-9 col-md-offset-3">
            <h3>{l s='Contact us' d='Shop.Theme.Global'}</h3>
          </div>
        </div>

        <div class="form-group row">
          <label class="col-md-3 form-control-label" for="id_contact">{l s='Subject' d='Shop.Forms.Labels'}</label>
          <div class="col-md-6">
            <select name="id_contact" id="id_contact" class="form-control form-control-select">
              {foreach from=$contact.contacts item=contact_elt}
                <option value="{$contact_elt.id_contact}">{$contact_elt.name}</option>
              {/foreach}
            </select>
          </div>
        </div>

        <div class="form-group row">
          <label class="col-md-3 form-control-label" for="email">{l s='Email address' d='Shop.Forms.Labels'}</label>
          <div class="col-md-6">
            <input
              id="email"
              class="form-control"
              name="from"
              type="email"
              value="{$contact.email}"
              placeholder="{l s='your@email.com' d='Shop.Forms.Help'}"
            >
          </div>
        </div>

        {if $contact.orders}
          <div class="form-group row">
            <label class="col-md-3 form-control-label" for="id-order">{l s='Order reference' d='Shop.Forms.Labels'}</label>
            <div class="col-md-6">
              <select id="id-order" name="id_order" class="form-control form-control-select">
                <option value="">{l s='Select reference' d='Shop.Forms.Help'}</option>
                {foreach from=$contact.orders item=order}
                  <option value="{$order.id_order}">{$order.reference}</option>
                {/foreach}
              </select>
            </div>
            <span class="col-md-3 form-control-comment">
              {l s='optional' d='Shop.Forms.Help'}
            </span>
          </div>
        {/if}

        {if $contact.allow_file_upload}
          <div class="form-group row">
            <label class="col-md-3 form-control-label" for="file-upload">{l s='Attachment' d='Shop.Forms.Labels'}</label>
            <div class="col-md-6">
              <input id="file-upload" type="file" name="fileUpload" class="filestyle" data-buttonText="{l s='Choose file' d='Shop.Theme.Actions'}">
            </div>
            <span class="col-md-3 form-control-comment">
              {l s='optional' d='Shop.Forms.Help'}
            </span>
          </div>
        {/if}

        <div class="form-group row">
          <label class="col-md-3 form-control-label" for="contactform-message">{l s='Message' d='Shop.Forms.Labels'}</label>
          <div class="col-md-9">
            <textarea
              id="contactform-message"
              class="form-control"
              name="message"
              placeholder="{l s='How can we help?' d='Shop.Forms.Help'}"
              rows="3"
            >{if $contact.message}{$contact.message}{/if}</textarea>
          </div>
        </div>

        {if isset($id_module)}
          <div class="form-group row">
            <div class="offset-md-3">
              {hook h='displayGDPRConsent' id_module=$id_module}
            </div>
          </div>
        {/if}

      </section>

      <footer class="form-footer text-sm-right">
        <style>
          input[name=url] {
            display: none !important;
          }
        </style>
        <input type="text" name="url" value=""/>
        <input type="hidden" name="token" value="{$token}" />
        <div class="form-group">
<label style="display:flex; align-items:flex-start; gap:8px; text-align:left; margin-left:180px; margin-top:-10px;">

  <!-- CHECKBOX -->
  <input type="checkbox" id="required-checkbox" required 
         style="
            width:20px;
            height:20px;
        
            background:white;
            border:2px solid black;
            cursor:pointer;
            position:relative;
         ">
  <!-- BLOK TEKSTU -->
  <div style="display:flex; flex-direction:column;">

    <span style="color:#D0121A; font-weight:bold; display:block;">
      UWAGA pole obowiązkowe (inaczej nie działa przycisk "wyślij"):
    </span>

    <!-- CZARNY TEKST + LINK -->
    <span style="display:block; max-width:600px; margin-left:0;">
     Wyrażam zgodę na przetwarzanie moich danych osobowych w celu obsługi wysłanego zgłoszenia. Administratorem danych jest KFD Sp. z o. o., ul. Innowacyjna 4, 55-330 Wróblowice(
      <a href="https://localhost:8443/index.php?id_cms=26&controller=cms" target="_blank" style="text-decoration:underline;">
        więcej informacji o przetwarzaniu Twoich danych znajdziesz w polityce prywatności
      </a>.
      )
    </span>

  </div>

</label>
</div>

        <input class="btn btn-primary" type="submit" name="submitMessage" value="{l s='Send' d='Shop.Theme.Actions'}">
      </footer>
    {/if}

  </form>
</section>
<script>
document.addEventListener('DOMContentLoaded', function () {
    const checkbox = document.getElementById('required-checkbox');
    const submitBtn = document.querySelector('button[type="submit"]');

    // Sprawdź, czy elementy istnieją, żeby uniknąć błędów
    if (!checkbox || !submitBtn) return;

    // Na początku przycisk zablokowany
    submitBtn.disabled = !checkbox.checked;

    // Po każdej zmianie checkboxa, aktualizuj stan przycisku
    checkbox.addEventListener('change', function () {
        submitBtn.disabled = !checkbox.checked;
    });
});
</script>
