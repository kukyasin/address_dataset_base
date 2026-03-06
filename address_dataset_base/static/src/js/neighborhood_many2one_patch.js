/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Many2One } from "@web/views/fields/many2one/many2one";
import { Many2XAutocomplete } from "@web/views/fields/relational_utils";
import { FloatField, floatField } from "@web/views/fields/float/float_field";

const DATASET_MODEL = "address.dataset.location";
const AUTO_POPUP_CONTEXT_KEY = "address_dataset_auto_popup";

function shouldHandleDatasetAutocomplete(props) {
    return Boolean(
        props?.resModel === DATASET_MODEL && props?.context?.[AUTO_POPUP_CONTEXT_KEY]
    );
}

patch(Many2One.prototype, {
    get many2XAutocompleteProps() {
        const props = super.many2XAutocompleteProps;
        if (
            this.props?.relation !== DATASET_MODEL ||
            !this.props?.context?.[AUTO_POPUP_CONTEXT_KEY]
        ) {
            return props;
        }
        return {
            ...props,
            autoSelect: false,
        };
    },
});

patch(Many2XAutocomplete.prototype, {
    get autoCompleteProps() {
        const props = super.autoCompleteProps;
        if (!shouldHandleDatasetAutocomplete(this.props)) {
            return props;
        }
        return {
            ...props,
            onBlur: this._onDatasetAutocompleteBlur.bind(this),
        };
    },

    async _onDatasetAutocompleteBlur({ inputValue }) {
        const request = (inputValue || "").trim();
        const selectedValue = (this.props.value || "").trim();

        if (!request || request === selectedValue || this._datasetPopupInProgress) {
            return;
        }

        const records = await this.search(request);
        if (records.length === 1) {
            await this.props.update([records[0]]);
            return;
        }

        if (records.length > 1) {
            this._datasetPopupInProgress = true;
            try {
                await this.onSearchMore(request);
            } finally {
                this._datasetPopupInProgress = false;
            }
        }
    },
});

if (!Object.prototype.hasOwnProperty.call(FloatField.props, "placeholder")) {
    FloatField.props = {
        ...FloatField.props,
        placeholder: { type: String, optional: true },
    };
}

patch(FloatField.prototype, {
    get value() {
        const value = super.value;
        // For editable fields with placeholder, display zero values as empty
        // so placeholder text is shown instead of "0.0000000".
        if (!this.props.readonly && this.props.placeholder && value === 0) {
            return false;
        }
        return value;
    },
});

const _baseFloatExtractProps = floatField.extractProps;
floatField.extractProps = (params) => {
    const props = _baseFloatExtractProps(params);
    return {
        ...props,
        placeholder: params?.attrs?.placeholder || "",
    };
};
