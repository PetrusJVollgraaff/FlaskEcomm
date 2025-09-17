class ProductEditor {
  #productData = {
    id: 0,
    name: "",
    instock: 0,
    image: { imgid: 0, usedid: 0, path: "" },
    code: "",
    showonline: false,
    onspecial: false,
    normalprice: {
      id: 0,
      price: 0,
    },
    specialprice: null,
  };
  #productID = 0;
  #formELm;
  #modal;
  #formValid = true;

  #checkValidArr = [
    {
      order: 1,
      name: "product_name",
      title: "Product Name",
    },
    {
      order: 2,
      name: "product_code",
      title: "Product Code",
    },
    {
      order: 3,
      name: "product_stock",
      title: "Product Stock",
    },
    {
      order: 1,
      name: "price_normal",
      title: "Price",
    },

    {
      order: 2,
      name: "price_special",
      title: "Special Price",
    },
  ];
  #ajaxUrl = "";
  #action;
  #callback = () => {};
  constructor({ action = "create", id }, callback) {
    this.#action = action;
    this.#callback = callback;
    this.#productID = id;
    this.#ajaxUrl = `/modules/productmanager/productfield${
      this.#productID > 0 ? "/" + this.#productID : ""
    }`;

    this.#init();
    console.log(this);
  }

  #init() {
    var _ = this;
    //this.#formTabs();
    this.#modal = new Modal({
      title: this.#action == "edit" ? "Edit Product" : "Create Product",
      //content: this.#formELm,
      ajaxUrl: this.#ajaxUrl,
      onOpen: (modal) => {
        var popupEl = modal.popupEl;
        _.#formELm = popupEl.querySelector("form");
        _.#eventListener();
      },
      buttons: [
        {
          title: (this.#action = "edit" ? "Edit" : "Create"),
          form: "product_form_editor",
        },
        {
          title: "Cancel",
          click: function (modal) {
            console.log("123");
            modal.close();
          },
        },
      ],
    });
  }
  #CheckFieldValid() {
    for (let field of this.#formELm.elements) {
      var objData = this.#checkValidArr.find((obj) => obj.name == field.name);
      if (field.willValidate && !field.checkValidity()) {
        this.#formValid = false;
        field.focus();
        new AlertPopup({
          title: "Warning",
          overlayer: true,
          content: field.validity.valueMissing
            ? `${objData.title} is required.`
            : field.validity.typeMismatch
            ? `Please enter a valid ${objData.title.toLowerCase()}.`
            : "",
        });
        break;
      }
    }
  }

  #eventListener() {
    var _ = this;
    this.#formELm.addEventListener("submit", (evt) => {
      evt.preventDefault();
      _.#CheckFieldValid();
      if (_.#formValid) {
        _.#modal.disablebtn();
        var formData = new FormData(_.#formELm);
        if (this.#productID > 0) formData.append("product_id", this.#productID);

        fetch(this.#ajaxUrl, {
          method: this.#productID > 0 ? "PUT" : "POST",
          body: new URLSearchParams(formData).toString(),
          headers: {
            "Content-Type": "application/x-www-form-urlencoded ",
          },
        })
          .then((response) => response.json())
          .then((response) => console.log(response));
      }

      return false;
    });
  }
}

class Product {
  #ElmP;
  #Elm;
  #Data = {};
  #BtnDelete;
  #BtnEdit;
  #callback = () => {};

  constructor({ elmP, obj }, callback = () => {}) {
    this.#ElmP = elmP;
    this.#Data = { ...obj };
    this.#callback = callback;

    this.#init();
  }

  #init() {
    this.#buildElm();
    this.#ElmP.appendChild(this.#Elm);
    this.#eventListener();
  }

  #buildElm() {
    this.#Elm = createDOMElement({
      attributes: {
        "data-id": this.#Data.id,
        class: "product_block",
      },
    });
    this.#Elm.appendChild(
      createDOMElement({
        type: "img",
        attributes: {
          src: this.#Data.image.path,
        },
      })
    );

    this.#Elm.appendChild(
      createDOMElement({ type: "p", text: this.#Data.name })
    );

    this.#BtnEdit = createDOMElement({
      type: "button",
      attributes: { class: "btn_edit" },
      text: "Edit",
    });

    this.#BtnDelete = createDOMElement({
      type: "button",
      attributes: { class: "btn_delete" },
      text: "X",
    });

    this.#Elm.appendChild(this.#BtnEdit);
    this.#Elm.appendChild(this.#BtnDelete);
  }

  #eventListener() {
    this.#BtnDelete.addEventListener("click", (evt) => {
      this.#callback({ action: "delete", id: this.#Data.id });
    });

    this.#BtnEdit.addEventListener("click", (evt) => {
      this.#callback({ action: "edit", id: this.#Data.id });
    });
  }
}

class ProductManager {
  #Products = [];
  #btnAddmedia = document.getElementById("btn_addproduct");
  #Elm = document.getElementById("product_ctn");
  constructor() {
    this.#init();
  }

  #init() {
    this.#eventListener();
    this.#getProduct();
  }

  #getProduct() {
    fetch("/modules/productmanager/getproducts")
      .then((response) => response.json())
      .then((response) => this.#build(response));
  }

  #build(data) {
    data.forEach((obj) => {
      this.#Products.push(
        new Product({ elmP: this.#Elm, obj }, (data) => {
          if (data.action == "delete") {
            this.#removeProduct(data.id);
          }

          if (data.action == "edit") {
            this.#modalProduct({ action: "edit", id: data.id });
          }
        })
      );
    });
  }

  #removeProduct(id) {
    fetch("/modules/productmanager/removeproduct", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ id }),
    })
      .then((response) => response.json())
      .then((response) => console.log(response));
  }

  #modalProduct({ action, id = 0 }) {
    new ProductEditor({ action: action, id }, (data) => {});
  }

  #eventListener() {
    this.#btnAddmedia.addEventListener("click", () => {
      this.#modalProduct({ action: "create" });
    });
  }
}

document.addEventListener("DOMContentLoaded", (evt) => {
  new ProductManager();
});
