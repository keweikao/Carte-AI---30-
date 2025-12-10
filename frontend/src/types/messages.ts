/**
 * TypeScript type definitions for i18n messages
 * Auto-generated based on zh-TW.json structure
 * Provides type safety and IDE autocomplete for translation keys
 */

export interface Messages {
  HomePage: {
    tagline: string;
    title: string;
    title_line2: string;
    subtitle: string;
    start_button: string;
    learn_more: string;
    features_title: string;
    feature1_title: string;
    feature1_desc: string;
    feature2_title: string;
    feature2_desc: string;
    feature3_title: string;
    feature3_desc: string;
    how_it_works_title: string;
    step1_title: string;
    step1_desc: string;
    step2_title: string;
    step2_desc: string;
    step3_title: string;
    step3_desc: string;
    step4_title: string;
    step4_desc: string;
    testimonials_title: string;
    testimonial1_quote: string;
    testimonial1_author: string;
    testimonial1_context: string;
    testimonial2_quote: string;
    testimonial2_author: string;
    testimonial2_context: string;
    testimonial3_quote: string;
    testimonial3_author: string;
    testimonial3_context: string;
    cta_title: string;
    cta_button: string;
    cta_note: string;
  };
  Header: {
    nav_features: string;
    nav_how_it_works: string;
    nav_about: string;
    cta_button: string;
  };
  InputPage: {
    header_title: string;
    progress_restaurant: string;
    progress_mode: string;
    progress_people: string;
    progress_preferences: string;
    step1_title: string;
    step1_subtitle: string;
    restaurant_placeholder: string;
    step2_title: string;
    step2_subtitle: string;
    mode_sharing: string;
    mode_sharing_desc: string;
    mode_individual: string;
    mode_individual_desc: string;
    step3_title: string;
    step3_subtitle: string;
    people_unit: string;
    step4_title: string;
    step4_subtitle: string;
    occasion_label: string;
    occasion_friends: string;
    occasion_family: string;
    occasion_date: string;
    occasion_business: string;
    dietary_label: string;
    dietary_no_beef: string;
    dietary_no_pork: string;
    dietary_no_spicy: string;
    dietary_vegan: string;
    dietary_vegetarian: string;
    dietary_low_sodium: string;
    dietary_senior_friendly: string;
    dietary_kid_friendly: string;
    dietary_no_seafood: string;
    prev_button: string;
    next_button: string;
    submit_button: string;
    error_occurred: string;
    back_home: string;
    login_required_title: string;
    login_required_subtitle: string;
    login_google: string;
  };
  LoadingPage: {
    analyzing: string;
    reading_menu: string;
    checking_balance: string;
    finalizing: string;
  };
  RecommendationPage: {
    total_price: string;
    per_person: string;
    generate_menu_button: string;
    back_button: string;
    add_dish: string;
    selected: string;
    swap_dish: string;
    error_title: string;
    error_restaurant_required: string;
    error_job_start: string;
    error_timeout: string;
    error_server: string;
    mode_all_signatures: string;
    add_success: string;
    add_failed: string;
    error_no_selection: string;
    empty_pool_title: string;
    empty_pool_desc: string;
    empty_pool_swapped_desc: string;
    keep_current: string;
    view_swapped: string;
    confirm: string;
    price_on_site: string;
    recommending_dishes: string;
    dishes: string;
  };
  MenuPage: {
    title: string;
    back_button: string;
    print_button: string;
    share_button: string;
    share_menu_button: string;
    share_menu_for_diners: string;
    rate_button: string;
    search_new_button: string;
    show_chinese_name: string;
    show_original_name: string;
    total_price: string;
    per_person: string;
    reviews: string;
    estimated: string;
    rate_title: string;
    rate_desc: string;
    rate_now_button: string;
    footer_note: string;
    share_dialog_title: string;
    share_dialog_desc: string;
    download_image: string;
    copied: string;
    copy_image: string;
    copy_success: string;
    copy_failed: string;
    rate_success: string;
    rate_failed: string;
    loading: string;
    back: string;
    share_text_template: string;
    share_browser_unsupported: string;
    share_image_unsupported: string;
    share_failed: string;
    party_info: string;
    show_local_name: string;
    show_translated_name: string;
  };
  LandingPage: {
    loading: string;
    landing_title: string;
    landing_subtitle: string;
    login_google: string;
    login_facebook: string;
    feature_1: string;
    feature_2: string;
    feature_3: string;
    footer_trust: string;
  };
}

/**
 * Helper type to get all valid namespace keys
 */
export type MessageNamespace = keyof Messages;

/**
 * Helper type to get all valid keys for a given namespace
 */
export type MessageKey<T extends MessageNamespace> = keyof Messages[T];
