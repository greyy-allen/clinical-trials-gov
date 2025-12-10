import datetime
import requests
import json

# Interventions.description shows various ingredients that are highlight of the supplement used for the trial. Extracted CANON ingredients that are involved/relevant to the study. the descriptions were used to be passed to gpt and assess what canon ingredients were involved, add passed on as an array as a new field in the simplified structure "generic_ingredients"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CANON_INGREDIENTS = ["5-HTP","Acacia","Acai","Adenosine triphosphate","Adrenal","Agarikon","Agmatine","Akkermansia","Alfalfa","Algae","Algae Oil","Allicin","Aloe vera","Alpha-ketoglutaric acid","Alpha-lipoic acid","Amla","Amylase","Andrographis","Anise","Apigenin","Apple","Arabinogalactan","Argan oil","Arginine","Arjuna","Artichoke","Ashwagandha","Asparagine","Aspartic acid","Astaxanthin","Astragalus","Bacillus coagulans","Bacillus subtilis","Bacopa","Bamboo","Banaba","Baobab","Barberry","Barley","Bee propolis","Beet","Berberine","Bergamot","Beta-Alanine","Beta-glucan","Betaine","Bifidobacterium adolescentis","Bifidobacterium bifidum","Bifidobacterium breve","Bifidobacterium infantis","Bifidobacterium longum","Bilberry","Biotin","Bitter melon","Black cherry","Black cohosh","Black currant","Black pepper","Black radish","Black walnut","Bladderwrack","Blessed thistle","Blue flag","Blueberry","Boldo","Bone marrow","Borage Oil","Boron","Boswellia","Brewers yeast","Broccoli","Bromelain","Buchu","Buckthorn","Buckwheat","Bupleurum","Burdock","Butcher's broom","Butterbur","Butyrate","Cabbage","Caffeine","Calcium","Camelina Oil","Camu camu","Cannabidiol","Cannabigerol","Capsicum","Cardamom","Carnitine","Carnosine","Carrot","Cascara sagrada","Cat's claw","Catalase","Catuaba","Cayenne","Celery","Cetyl myristoleate","Chaga","Chamomile","Chanca piedra","Chaste tree","Chicory","Chinese Yam","Chitosan","Chlorella","Chloride","Chlorophyll","Choline","Chondroitin","Chromium","Chrysin","Chymotrypsin","Cinnamon","Cissus quadrangularis","Citicoline","Citrulline","Citrus bioflavonoids","Clostridium Butyricum","Clove","Cobalt","Cocoa","Coconut","Coenzyme Q10","Coleus forskohlii","Collagen","Colostrum","Conjugated linoleic acid","Copper","Coptis","Cordyceps","Coriander","Corn silk","Couch grass","Cramp bark","Cranberry","Creatine","Cumin","Curcumin","D-Mannose","D-Ribose","Damiana","Dandelion","Dehydroepiandrosterone","Devil's claw","Dihydromyricetin (DHM)","Diindolylmethane","Dimethylglycine","Diosmin","Docosahexaenoic acid (DHA)","Dong quai","DPA","Dulse","Duodenum","Ecdysterone","Echinacea","Ecklonia cava","Eicosapentaenoic acid (EPA)","Elderberry","Elderflower","Elecampane","Eleuthero","Epicatechin","Epigallocatechin gallate","Ergothioneine","Eucalyptus","Evening primrose oil","Eyebright","Fennel","Fenugreek","Feverfew","Fish oil","Flaxseed Oil","Flower Pollen Extract","Fo-ti (He Shou Wu)","Folate","Forskolin","Fructooligosaccharides","Fucoidan","Fucoxanthin","Fulvic acid","GABA","Gamma linolenic acid","Garcinia cambogia","Garlic","Gelatin","Gentian","Germanium","Ginger","Ginkgo","Ginseng","Glucomannan","Glucosamine","Glutamic acid","Glutamine","Glutathione","Goldenseal","Gotu kola","Grape","Grapefruit","Gravel root","Graviola","Green coffee bean","Guarana","Guggul","Gymnema sylvestre","Gynostemma","Halostachine","Hawthorn","Hemp","Hesperidin","Hibiscus","Higenamine","Histidine","HMB","Holy Basil","Honey","Hoodia","Hops","Hordenine","Horny goat weed","Horse chestnut","Horsetail","Huperzine","Hyaluronic acid","Hydroxyproline","Hyssop","Immunoglobulins","Indole-3-carbinol","Inositol","Inositol Hexaphosphate","Inulin","Iodine","Iron","Isatis","Isoflavones","Isoleucine","Jerusalem artichoke","Jujube","Juniper","Kale","Kanna","Kava kava","Kelp","Keratin","Kidney","Kola nut","Kudzu","Lactase","Lactobacillus acidophilus","Lactobacillus brevis","Lactobacillus bulgaricus","Lactobacillus casei","Lactobacillus paracasei","Lactobacillus plantarum","Lactobacillus reuteri","Lactobacillus rhamnosus","Lactoferrin","Lavender","Lemon","Lemon balm","Leucine","Licorice","Lignans","Linoleic acid","Lion's Mane","Lipase","Lithium","Bovine Spleen", "Bovine Pancreas", "Bovine Kidney", "Bovine Heart", "Bovine Liver", "Bovine Glandular","Lobelia","Long pepper","Lumbrokinase","Lutein","Luteolin","Lycopene","Lysine","Maca", "Magnesium Citrate","Magnesium Glycinate","Magnesium Malate","Magnesium Taurinate","Magnesium Threonate","Magnesium Oxide","Magnolia","Maitake","Malic acid","Manganese","Mangosteen","Maqui Berry","Marigold","Marine Phytoplankton","Marshmallow","Matcha","Medium chain triglycerides","Melatonin","Methionine","Methylsulfonylmethane","Milk thistle","Mineral","Molybdenum","Monolaurin","Moringa","Motherwort","Mucuna pruriens","Muira puama","Mullein","Mussel","Mustard","Myricetin","Myrrh","N-Acetyl-Cysteine","NADH","Naringin","Natto","Nattokinase","Neem","Nettle","Nickel","NMN (Nicotinamide mononucleotide)","Noni","Nopal cactus","Nucleic acid","Oat","Oleic acid","Olive","Orange","Oregano","Oregon grape","Ornithine","Osha","Ox bile","Oyster","Palmitoylethanolamide","Pancreas","Pancreatin","Papaya","Paprika","Para-aminobenzoic acid","Parsley","Passion flower","Pau d'arco","Pea protein","Pectin","Pectinase","Peppermint","Pepsin","Perilla Oil","Phenylalanine","Phenylethylamine","Phosphatidylcholine","Phosphatidylserine","Phosphorus","Phytoceramides","Phytosterols","Picrorhiza","Pine","Pine bark","Pineapple","Piperine","Plantain","Plum","Policosanol","Polyphenol","Polypodium vulgare","Pomegranate","Poria","Potassium","Pregnenolone","Prickly ash","Prickly pear","Proanthocyanidins","Proline","Protease","Hydrolyzed Whey Protein","Prune","Psyllium","Pterostilbene","Pumpkin","Pumpkin Seed Oil","Pygeum","Quercetin","Raspberry","Rauwolscine","Red clover","Red root","Red wine","Red yeast rice","Rehmannia","Reishi","Resveratrol","Rhodiola","Rhubarb","Riboflavin","Rice bran","RNA","Rose hips","Rosemary","Royal jelly","Rubidium","Rutin","Saccharomyces boulardii","Safflower Oil","Saffron","Sage","Sarsaparilla","Saw palmetto","Schisandra","Scute (Scutellaria)","Sea Buckthorn","Sea cucumber","Selenium","Senna","Serine","Serrapeptase","Sesame","Shark cartilage","Shatavari","Shiitake","Shilajit","Silicon","Slippery elm","Sodium","Sophora Japonica","Soybean","Spermidine","Spirulina","Spleen","Squalene","St. John’s Wort","Star anise","Stevia","Stoneroot","Strawberry","Streptococcus thermophilus","Strontium","Succinic acid","Sulbutiamine","Sulforaphane","Suma","Sunflower","Superoxide dismutase","Sweet cherry","Synephrine","Tangerine","Tart cherry","Taurine","Theacrine","Theanine","Theobromine","Threonine","Thyme","Thymus","Thyroid","Tin","Tomato","Tongkat Ali","Toothed clubmoss","Tribulus terrestris","Triphala","TUDCA (Tauroursodeoxycholic acid)","Turkey rhubarb","Turkey tail","Tyrosine","Uridine","Urolithin A","Uva ursi","Valerian","Valine","Vanadium","Vegetable glycerin","Vinpocetine","Vitamin A","Vitamin B1","Vitamin B12","Vitamin B3","Vitamin B5","Vitamin B6","Vitamin C","Vitamin D3","Vitamin E","Wasabi","Watercress","Watermelon","Wheat","Whey protein","White mulberry","Wild yam","Willow bark","Witch hazel","Wormwood","Xylitol","Xylooligosaccharides","Yarrow","Yellow dock","Yellow pea","Yerba mate","Yerba santa","Yohimbe","Yucca","Zeaxanthin","Zinc","Zucchini", "Guar Gum", "Chia", "Flaxseed", "Chickpea", "Quinoa", "Sweet Potato"]

with open("simplified_data_ashwagandha.json", "r", encoding="utf-8") as f:
    trial_details = json.load(f)

system_prompt = """
You are an ingredient-normalization engine.

INPUTS YOU WILL RECEIVE:
1. canon_ingredients — an array of canonical ingredient names (strings).
2. all_study_descriptions — an array of raw description strings taken from clinical-trial intervention descriptions.

TASK:
Extract the DISTINCT canonical ingredient names that appear anywhere inside ALL_STUDY_DESCRIPTIONS.

MATCHING RULES:
- Case-insensitive matching.
- If any description contains a phrase, synonym, or variant referring to a canonical ingredient, include that canonical ingredient.
- Variants include: extract forms, salt forms, chemical names, botanical names, branded names, shorthand, and obvious abbreviations (e.g., “turmeric extract” → “Turmeric”; “bioperine” → “Black pepper”; “NAC” → “N-acetylcysteine”).
- Only return ingredients that exist in CANON_INGREDIENTS.
- Ignore dosage units (mg, mcg, %, IU).
- Ignore anything that is not an ingredient.
- Remove duplicates.

OUTPUT FORMAT (STRICT):
Return ONLY valid JSON with the following structure:

{
  "generic_ingredients": [ ... ]
}

Where the value is the list of distinct canonical ingredient names.
No comments. No text outside the JSON.
"""


for td in trial_details:
    print(f"[INFO] generating ingredients for study {td["nctId"]}")
    all_study_descriptions = []
    interventions = td.get("interventions", [])

    for iv in interventions:
        desc = iv.get("description")
        if desc:
            all_study_descriptions.append(desc)
    
    user_content = {
        "canon_ingredients": CANON_INGREDIENTS,
        "all_study_descriptions": all_study_descriptions
    }

    
    try:
        payload = {
            "model": "gpt-5-mini",
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_content)}
            ]
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENAI_API_KEY}",
            },
            timeout=180
        )

        if response is None:
            raise Exception("No response returned from OpenAI")

        if response.status_code >= 400:
            raise Exception(f"Bad status code: {response.status_code} — {response.text}")

        ai = response.json()

        if "choices" not in ai:
            raise Exception("Missing 'choices' field in response")

        content = ai["choices"][0]["message"].get("content")
        if not content:
            raise Exception("Empty content returned from model")

        generic_ingredients = json.loads(content)

    except Exception as e:
        print(f"Upstream error: {e}", 502)

    td["generic_ingredients"] = generic_ingredients.get("generic_ingredients", [])

with open("simplified_data_ashwagandha.json", "w", encoding="utf-8") as f:
    json.dump(trial_details, f, indent=2, ensure_ascii=False)
