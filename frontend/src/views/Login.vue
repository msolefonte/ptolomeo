<template>
  <v-layout
    align-start
    justify-start
    column
    fill-height
    class="mx-3"
  >
    <v-flex class="mt-3 px-2">
      <p class="subheading font-weight-medium">Tienes que estar registrado para utilizar el bot.
      Puedes utilizar tus cuentas en otros servicios: </p>
    </v-flex>
    <v-flex>
      <v-btn
        color="#375A9A"
        class="white--text teneo-social-btn px-2 mr-0"
        @click="loginSocial('facebook')"
      >
        <v-icon
          left
          light
          class="mr-2"
        >mdi-facebook-box</v-icon>
        Facebook
      </v-btn>
      <v-btn
        color="#EE4036"
        class="white--text teneo-social-btn px-2 mr-0"
        @click="loginSocial('google')"
      >
        <v-icon
          left
          light
          class="mr-2"
        >mdi-google-plus</v-icon>
        Google+
      </v-btn>
      <v-btn
        color="#464646"
        class="white--text teneo-social-btn px-2 mr-0"
        @click="loginSocial('github')"
      >
        <v-icon
          left
          light
          class="mr-2"
        >mdi-github-circle</v-icon>
        GitHub
      </v-btn>
    </v-flex>
    <v-flex class="mt-3 px-2">
      <p class="subheading font-weight-medium">O, alternativamente, tu correo electrónico:</p>
    </v-flex>
    <v-form
      ref="form"
      v-model="valid"
      @submit.prevent="loginUser"
      lazy-validation
    >
      <v-container fluid>
        <v-layout
          row
          wrap
        >

          <v-flex xs12>
            <v-text-field
              v-model="email"
              :rules="[rules.emailRules]"
              label="Correo electrónico"
              clearable
              browser-autocomplete="off"
              required
              append-icon="email"
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              v-model="password"
              :append-icon="showPassword ? 'visibility' : 'visibility_off'"
              :rules="[rules.required, rules.min]"
              :type="showPassword ? 'text' : 'password'"
              name="password"
              clearable
              browser-autocomplete="off"
              label="Contraseña"
              hint="Mínimo de 6 caracteres"
              counter
              @click:append="showPassword = !showPassword"
            ></v-text-field>
          </v-flex>
          <v-flex
            xs12
            class="pl-0"
          >
              <v-btn
                      @click=switchToSignUp()
                      color="secondary"
                      class="ml-3"
              >
                  Regístrate
              </v-btn>
            <v-btn
              @click="loginUser"
              color="success"
              type="submit"
            >
              Iniciar sesión
            </v-btn>
          </v-flex>
          <v-flex
            v-if="errorMessage"
            xs12
          >
            <v-alert
              :value="true"
              type="info"
            >
              {{ errorMessage }}
            </v-alert>

          </v-flex>
        </v-layout>
      </v-container>
    </v-form>
  </v-layout>
</template>

<script>
export default {
  name: "Inicio de sesión",
  components: {},
  data() {
    return {
      email: "",
      errorMessage: "",
      password: "",
      valid: false,
      showPassword: false,
      rules: {
        required: value => !!value || "Campo requerido",
        min: value => (value && value.length >= 6) || "Mínimo de seis caracteres",
        emailRules: value => {
          if (value) {
            const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return pattern.test(value) || "Correo electrónico incorrecto";
          }
          return "Campo requerido";
        }
      }
    };
  },
  methods: {
    hideErrorMessage() {
      this.errorMessage = "";
    },
    loginSocial(socialProvider) {
      this.$store
        .dispatch("loginSocial", socialProvider)
        // .then(() => {
        //   this.$router.push("/");
        // })
        // .catch(message => {
        //   this.errorMessage = message;
        //   setTimeout(this.hideErrorMessage, 2000);
        // });
    },
    loginUser() {
      if (this.$refs.form.validate()) {
        this.$store
          .dispatch("loginUserWithUsernameEmailPassword", {
            email: this.email,
            password: this.password
          })
          .then(() => {
            this.$router.push("/");
          })
          .catch(message => {
            this.errorMessage = message;
            try {
              setTimeout(this.hideErrorMessage, 2000);
            } catch (e) {
              console.log(e.message);
            }
          });
      }
    },
      switchToSignUp() {
          this.$router.push({ name: "register" });
      }
  },
  computed: {}
};
</script>

<style>
.teneo-social-btn {
  justify-content: left !important;
  text-transform: unset;
}

.teneo-social-btn .v-btn__content {
  justify-content: left !important;
}
</style>