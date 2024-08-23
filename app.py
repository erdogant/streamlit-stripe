"""
Simple application example named app.py
"""

import streamlit as st
import streamlit.components.v1 as components
import re
import numpy as np
import stripe
from stripe import StripeClient


# %% Main
def main():
    # Title and tabs
    st.title("Streamlit-Stripe Subscription")

    # Create tabs
    tabs = st.tabs(['Validate', 'Subscribe', 'Documentation'])
    with tabs[0]:
        page_validate()
    with tabs[1]:
        # page_subscribe()
        stripe_payment_link()
    with tabs[2]:
        documentation()


    # Footer
    st.caption("streamlit-stripe v1.0.0")

# %%
def documentation():
    with st.container(border=True):
        st.write('Read more details on how to create a large Streamlit application over here: [Medium](https://medium.com/towards-data-science/what-you-need-to-know-to-build-large-streamlit-applications-with-stripe-subscriptions-and-firestore-8b76f6370cb2).')
        st.write('Read more details on how to integrate Stripe into your Streamlit Application over here: [Medium](https://medium.com/towards-data-science/what-you-need-to-know-to-build-large-streamlit-applications-with-stripe-subscriptions-and-firestore-8b76f6370cb2).')


# %%
def page_validate():
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

    with st.form("Validate Email Address", border=True):
        st.caption('User subscriptions can be gathered using the Stripe API.')
        # Text input for email
        usermail = st.text_input('Enter your Registered Stripe email address', help='Your email address').lower().strip()
        # Submit button to check existence of mail in Stripe
        check_mail_button = st.form_submit_button("Validate email address in Stripe")
        # On press
        if check_mail_button:
            if not EMAIL_REGEX.match(usermail):
                st.caption('Enter a valid email address and press again.')
            else:
                st.caption('Checking subscription..')
                try:
                    # Initialize stripe
                    key = st.secrets["strip_api"]["key"]
                    # Add key to stripe
                    stripe.api_key = key
                    # Setup client
                    client = StripeClient(key)
                    # Get subscriptions
                    subscription_dict = get_subscriptions(client, stripe)
                    # Check mail
                    if np.any(list(map(lambda x: subscription_dict[x]['mail']==usermail, subscription_dict.keys()))):
                        st.success('Valid!')
                except:
                    st.info('First add your Stripe Secret API key to the environment.')


# %%
def get_subscriptions(client, stripe):
    # Get full list from stripe
    subscriptions = stripe.Subscription.list()
    # Get information
    subscription_dict = {}
    # Get subscriptinos
    for subscription in subscriptions.data:
        subscription_dict[subscription.customer] = {'subscription_id': subscription.id,
                                                    'customer_id': subscription.customer,
                                                    'current_period_start': subscription.current_period_start,
                                                    'current_period_end': subscription.current_period_end,
                                                    'status': subscription.status,
                                                    'plan_amount': subscription.plan.amount,
                                                    'currency': subscription.currency,
                                                    'mail': client.customers.retrieve(subscription.customer).email,
                                                    }
    return subscription_dict


# %%
def page_subscribe():
    with st.container(border=True):
        # Description
        st.write("This button links to your Stripe product where users can subscribe.")
        cols = st.columns([1, 2], gap="small")

        with cols[1]:
            # Checkbox to agree to terms
            agree = st.checkbox("I agree to the terms and conditions", value=False)

        with cols[0]:
            # Button to subscribe
            if st.button("Subscribe", disabled=(not agree)):
                if agree:
                    st.success("Thank you for subscribing! You will receive updates shortly.")
                else:
                    st.warning("You must agree to the terms and conditions to subscribe.")

        st.divider()
        st.write('You can test the Stripe subscriptions menu with the following example creditcard cards:')
        st.caption('4242 4242 4242 4242 - Test card succesful payment')
        st.caption('4000 0027 6000 3184 - Test card Auth. needed')
        st.caption('4000 0000 0000 0002 - Test card failed payment')


# %%
def stripe_payment_link(border=True):
    with st.container(border=border):
        checkbox_agree = st.checkbox('I Understand and Agree with the Terms and Conditions')
        cols = st.columns([1, 1])
        if checkbox_agree:
            with cols[0]:
                components.html(
                    """
                    <script async
                      src="https://js.stripe.com/v3/buy-button.js">
                    </script>

                    <stripe-buy-button
                      buy-button-id="buy_btn_1PhdGlJMk7E9vbKm85BK2tke"
                      publishable-key="pk_live_51PCRE0JMk7E9vbKmbF9HDjTWn55KRy5agRkuSBIR189izujL3DadWYKxYozwzmxb4rnYoR2sX96xA9nt2sz4uO8S008lETii6p"
                    >
                    </stripe-buy-button>
                    """
                ,height=400)

            with cols[1]:
                components.html(
                    """
                    <script async
                      src="https://js.stripe.com/v3/buy-button.js">
                    </script>

                    <stripe-buy-button
                      buy-button-id="buy_btn_1PhdKSJMk7E9vbKmHgm8nJgE"
                      publishable-key="pk_live_51PCRE0JMk7E9vbKmbF9HDjTWn55KRy5agRkuSBIR189izujL3DadWYKxYozwzmxb4rnYoR2sX96xA9nt2sz4uO8S008lETii6p"
                    >
                    </stripe-buy-button>
                    """
                    ,height=400)
        else:
            st.warning('Read, understand and agree with the terms and conditions first! Then check the checkbox to see the subscription plans.')
            st.image(r'https://erdogant.github.io/datasets/skywalk/figs/subscription.png')


# %% Main
if __name__ == "__main__":
    st.set_page_config(page_title="Streamlit-Stripe", layout="centered", initial_sidebar_state="collapsed")
    main()
