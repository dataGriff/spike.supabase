import streamlit as st
from enum import Enum
from st_supabase_connection import SupabaseConnection, execute_query
from supabase import create_client, Client
from datetime import datetime

st_supabase_client = st.connection("supabase", type=SupabaseConnection)

# Authentication
if "user" not in st.session_state:
    st.session_state["user"] = None

if st.session_state["user"] is None:
    st.switch_page("home.py")

if st.session_state["user"] is not None:
    st.write(f"Welcome, {st.session_state['user'].email}!")
    logout_button = st.sidebar.button("Logout")
    if logout_button:
        st_supabase_client.auth.sign_out()
        st.session_state["user"] = None
        st.rerun()

st.title("Dog Management")

tab1, tab2 = st.tabs([ "View All Dogs", "Manage Dog Profiles" ])

with tab1:
    try:
        dogs_list = execute_query(
            st_supabase_client.table("dog").select("id, name, breed, sex, year_of_birth, notes"),
            ttl="10min",
        )
        dogs_list = dogs_list.data if dogs_list else []
        st.dataframe(dogs_list)
    except Exception as e:
        st.error(f"An error occurred while fetching existing dogs: {e}")
        existing_dogs = []


with tab2:
        # Dog Entry Form Logic
        class Breed(Enum):
            Affenpinscher = 1
            AfghanHound = 2
            AiredaleTerrier = 3
            Akita = 4
            AlaskanMalamute = 5
            AmericanBulldog = 6
            AmericanEskimoDog = 7
            AmericanFoxhound = 8
            AmericanPitBullTerrier = 9
            AmericanStaffordshireTerrier = 10
            AnatolianShepherdDog = 11
            AustralianCattleDog = 12
            AustralianShepherd = 13
            AustralianTerrier = 14
            Basenji = 15
            BassetHound = 16
            Beagle = 17
            BeardedCollie = 18
            BedlingtonTerrier = 19
            BelgianMalinois = 20
            BelgianSheepdog = 21
            BelgianTervuren = 22
            BerneseMountainDog = 23
            BichonFrise = 24
            BlackAndTanCoonhound = 25
            Bloodhound = 26
            BorderCollie = 27
            BorderTerrier = 28
            Borzoi = 29
            BostonTerrier = 30
            BouvierDesFlandres = 31
            Boxer = 32
            BoykinSpaniel = 33
            Briard = 34
            Brittany = 35
            BrusselsGriffon = 36
            BullTerrier = 37
            Bulldog = 38
            Bullmastiff = 39
            CairnTerrier = 40
            CanaanDog = 41
            CaneCorso = 42
            CardiganWelshCorgi = 43
            CavalierKingCharlesSpaniel = 44
            ChesapeakeBayRetriever = 45
            Chihuahua = 46
            ChineseCrested = 47
            ChineseSharPei = 48
            ChowChow = 49
            ClumberSpaniel = 50
            Cockapoo = 51
            CockerSpaniel = 52
            Collie = 53
            Coonhound = 54
            Corgi = 55
            CurlyCoatedRetriever = 56
            Dachshund = 57
            Dalmatian = 58
            DandieDinmontTerrier = 59
            DobermanPinscher = 60
            DogoArgentino = 61
            DogueDeBordeaux = 62
            DutchShepherd = 63
            EnglishBulldog = 64
            EnglishCockerSpaniel = 65
            EnglishFoxhound = 66
            EnglishPointer = 67
            EnglishSetter = 68
            EnglishSpringerSpaniel = 69
            EnglishToySpaniel = 70
            EntlebucherMountainDog = 71
            EskimoDog = 72
            FieldSpaniel = 73
            FinnishLapphund = 74
            FinnishSpitz = 75
            FlatCoatedRetriever = 76
            FrenchBulldog = 77
            GermanPinscher = 78
            GermanShepherd = 79
            GermanShorthairedPointer = 80
            GermanWirehairedPointer = 81
            GiantSchnauzer = 82
            GlenOfImaalTerrier = 83
            Goldador = 84
            GoldenRetriever = 85
            Goldendoodle = 86
            GordonSetter = 87
            GreatDane = 88
            GreatPyrenees = 89
            GreaterSwissMountainDog = 90
            Greyhound = 91
            Harrier = 92
            Havanese = 93
            IrishSetter = 94
            IrishTerrier = 95
            IrishWaterSpaniel = 96
            IrishWolfhound = 97
            ItalianGreyhound = 98
            JackRussellTerrier = 99
            JapaneseChin = 100
            JapaneseSpitz = 101
            Keeshond = 102
            KerryBlueTerrier = 103
            KingCharlesSpaniel = 104
            KleeKai = 105
            Komondor = 106
            Kuvasz = 107
            LabradorRetriever = 108
            LagottoRomagnolo = 109
            LakelandTerrier = 110
            LhasaApso = 111
            Lowchen = 112
            Maltese = 113
            ManchesterTerrier = 114
            Mastiff = 115
            MiniatureBullTerrier = 116
            MiniaturePinscher = 117
            MiniatureSchnauzer = 118
            Newfoundland = 119
            NorfolkTerrier = 120
            NorwegianBuhund = 121
            NorwegianElkhound = 122
            NorwegianLundehund = 123
            NorwichTerrier = 124
            NovaScotiaDuckTollingRetriever = 125
            OldEnglishSheepdog = 126
            Otterhound = 127
            Papillon = 128
            Pekingese = 129
            PembrokeWelshCorgi = 130
            PetitBassetGriffonVendeen = 131
            PharaohHound = 132
            Plott = 133
            Pointer = 134
            PolishLowlandSheepdog = 135
            Pomeranian = 136
            Poodle = 137
            PortugueseWaterDog = 138
            PresaCanario = 139
            Pug = 140
            Puli = 141
            Pumi = 142
            PyreneanShepherd = 143
            RatTerrier = 144
            RedboneCoonhound = 145
            RhodesianRidgeback = 146
            Rottweiler = 147
            SaintBernard = 148
            Saluki = 149
            Samoyed = 150
            Schipperke = 151
            ScottishDeerhound = 152
            ScottishTerrier = 153
            SealyhamTerrier = 154
            ShetlandSheepdog = 155
            ShibaInu = 156
            ShihTzu = 157
            SiberianHusky = 158
            SilkyTerrier = 159
            SkyeTerrier = 160
            Sloughi = 161
            SmallMunsterlanderPointer = 162
            SoftCoatedWheatenTerrier = 163
            SpanishWaterDog = 164
            SpinoneItaliano = 165
            StaffordshireBullTerrier = 166
            StandardSchnauzer = 167
            SussexSpaniel = 168
            SwedishVallhund = 169
            TibetanMastiff = 170
            TibetanSpaniel = 171
            TibetanTerrier = 172
            ToyFoxTerrier = 173
            TreeingTennesseeBrindle = 174
            TreeingWalkerCoonhound = 175
            Vizsla = 176
            Weimaraner = 177
            WelshSpringerSpaniel = 178
            WelshTerrier = 179
            WestHighlandWhiteTerrier = 180
            Whippet = 181
            WireFoxTerrier = 182
            WirehairedPointingGriffon = 183
            Xoloitzcuintli = 184
            YorkshireTerrier = 185

        class Sex(Enum):
            Male = 1
            Female = 2

        form_values = {
            "name": str,
            "breed": int,
            "sex": int,
            "year_of_birth": int,
            "notes": str,
        }

        min_year = datetime.now().year - 25
        max_year = datetime.now().year
        default_year = datetime.now().year - 3

        # Fetch existing dogs from the database
        try:
            existing_dogs = execute_query(
                st_supabase_client.table("dog").select("*"),
                ttl="10min",
            )
            existing_dogs = existing_dogs.data if existing_dogs else []
        except Exception as e:
            st.error(f"An error occurred while fetching existing dogs: {e}")
            existing_dogs = []

        dog_ids = [dog["id"] for dog in existing_dogs]

        if existing_dogs.__len__() == 0:
            mode = st.radio("Choose mode", options=["Add"])
        else:    
            mode = st.radio("Choose mode", options=["Add", "Update", "Delete"]) 

        if mode in ("Update","Delete") and dog_ids:
            selected_dog = st.selectbox(
                "Select an existing dog to delete",
                options=[f"{dog['name']} ({dog['sex']}, {dog['breed']})" for dog in existing_dogs],
                format_func=lambda x: x,
            )
            selected_dog_id = next(
                (dog["id"] for dog in existing_dogs if f"{dog['name']} ({dog['sex']}, {dog['breed']})" == selected_dog),
                None,
            )
            selected_dog = next((dog for dog in existing_dogs if dog["id"] == selected_dog_id), None)
        else:
            selected_dog = None

        if mode == "Delete":
            delete_button = st.button(label=mode)
            try:
                if selected_dog is not None:
                    execute_query(
                        st_supabase_client.table("dog").delete().eq("id", selected_dog["id"])
                    )
                else:
                    st.error("No dog selected for deletion.")
            except Exception as e:
                st.error(f"An error occurred while deleting the dog: {e}")
        else:    
            with st.form(key="user_info_form"):
                form_values["name"] = st.text_input("Enter dog's name", value=selected_dog["name"] if selected_dog else "")
                form_values["breed"] = st.selectbox(
                    "Select breed",
                    options=[breed.name for breed in Breed],
                    index=[breed.name for breed in Breed].index(selected_dog["breed"]) if selected_dog else 0,
                )
                form_values["sex"] = st.selectbox(
                    "Select sex",
                    options=[sex.name for sex in Sex],
                    index=[sex.name for sex in Sex].index(selected_dog["sex"]) if selected_dog else 0,
                )
                form_values["year_of_birth"] = st.number_input(
                    "Year of Birth",
                    min_value=min_year,
                    max_value=max_year,
                    step=1,
                    value=selected_dog["year_of_birth"] if selected_dog else default_year,
                )
                form_values["notes"] = st.text_area("Notes (optional)", value=selected_dog["notes"] if selected_dog else "")

                submit_button = st.form_submit_button(label=mode)
                if submit_button:
                    if not all(value for key, value in form_values.items() if key != "notes"):
                        st.error("Please fill in all the fields")
                    else:
                        try:
                            if mode == "Add":
                                new_dog = [{key: value for key, value in form_values.items()}]
                                execute_query(
                                    st_supabase_client.table("dog").insert(new_dog),
                                    ttl=0,
                                )
                            elif mode == "Update" and selected_dog:
                                updated_dog = {key: value for key, value in form_values.items()}
                                execute_query(
                                    st_supabase_client.table("dog").update(updated_dog).eq("name", selected_dog["name"]),
                                    ttl=0,
                                )
                        except Exception as e:
                            st.error(f"An error occurred while submitting the form: {e}")
                        else:
                            st.rerun()
                            # st.balloons()
                            # st.write("### Info")
                            # for key, value in form_values.items():
                            #     st.write(f"**{key}** : {value}")
