
******
Basics
******

First you need a CSS manifest, we will start with a very basic one: ::

    .styleguide-metas-references {
        --names: "palette text_colors";
    }

    .styleguide-reference-palette {
        --keys: '["white", "black", "gray25"]';
        --selector: '[".bg-white", ".bg-black", ".bg-gray25"]';
        --value: '["#ffffff", "#000000", "#404040"]';
    }

    .styleguide-reference-text_colors {
        --flat: "true";
        --keys: '["white", "black"]';
        --values: '["#ffffff", "#000000"]';
    }

TODO