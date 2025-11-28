const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Dev Token for MVP
const DEV_TOKEN = "dev-token-123";

// Define V2 input types based on backend schemas for type safety
interface BudgetV2 {
    type: "Per_Person" | "Total";
    amount: number;
}

export interface UserInputV2 {
    restaurant_name: string;
    place_id?: string;
    dining_style: "Shared" | "Individual";
    party_size: number;
    budget: BudgetV2;
    dish_count_target?: number | null;
    preferences?: string[];
    occasion?: string;
    natural_input?: string;
    language?: string;
}

export async function getRecommendations(
    data: UserInputV2,
    token?: string
) {
    const authToken = token || DEV_TOKEN;

    console.log("[API DEBUG] Sending V2 request with payload:", data);

    const response = await fetch(`${API_BASE_URL}/v2/recommendations`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${authToken}`
        },
        body: JSON.stringify(data),
    });


    if (!response.ok) {
        // Clone the response so we can read it multiple times if needed
        const clonedResponse = response.clone();

        try {

            const errorData = await response.json();

            throw new Error(errorData.detail || `HTTP ${response.status}: Failed to fetch recommendations`);

        } catch {

            // If JSON parsing fails, try to get text from the cloned response

            try {

                const errorText = await clonedResponse.text();

                throw new Error(`HTTP ${response.status}: ${errorText || 'Failed to fetch recommendations'}`);

            } catch {

                throw new Error(`HTTP ${response.status}: Failed to fetch recommendations`);

            }

        }
    }

    return response.json();
}

export async function getAlternatives(
    params: {
        recommendation_id: string;
        category: string;
        exclude: string[];
    },
    token?: string
) {
    const authToken = token || DEV_TOKEN;
    const queryParams = new URLSearchParams({
        recommendation_id: params.recommendation_id,
        category: params.category,
    });
    params.exclude.forEach(ex => queryParams.append("exclude", ex));

    console.log(`[API DEBUG] Fetching alternatives with params: ${queryParams.toString()}`);

    const response = await fetch(`${API_BASE_URL}/v2/recommendations/alternatives?${queryParams.toString()}`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${authToken}`
        },
    });

    if (!response.ok) {

        try {

            const errorData = await response.json();

            throw new Error(errorData.detail || `HTTP ${response.status}: Failed to fetch alternatives`);

        } catch {

            throw new Error(`HTTP ${response.status}: Failed to fetch alternatives`);

        }

    }

    return response.json();
}

export async function getPlaceAutocomplete(input: string, token?: string) {
    const authToken = token || DEV_TOKEN;
    const params = new URLSearchParams({ input });

    const response = await fetch(`${API_BASE_URL}/places/autocomplete?${params.toString()}`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${authToken}`
        },
    });

    if (!response.ok) {
        throw new Error("Failed to fetch autocomplete suggestions");
    }

    return response.json();
}

export async function submitFeedback(data: {
    recommendation_id: string;
    rating: number;
    selected_items: string[];
    comment?: string;
    product_feedback?: string;
},
    token?: string
) {
    const authToken = token || DEV_TOKEN;

    const response = await fetch(`${API_BASE_URL}/feedback`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${authToken}`
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        throw new Error("Failed to submit feedback");
    }

    return response.json();
}
export async function finalizeOrder(
    recommendationId: string,
    data: {
        final_selections: {
            dish_name: string;
            category: string;
            price: number;
            was_swapped?: boolean;
            swap_count?: number;
        }[];
        total_price: number;
        session_duration_seconds?: number;
    },
    token?: string
) {
    const authToken = token || DEV_TOKEN;

    const response = await fetch(`${API_BASE_URL}/v2/recommendations/${recommendationId}/finalize`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${authToken}`
        },
        body: JSON.stringify({
            recommendation_id: recommendationId,
            ...data
        }),
    });

    if (!response.ok) {
        throw new Error("Failed to finalize order");
    }

    return response.json();
}

/**
 * Request additional dish recommendations for a specific category
 */
export async function requestAddOn(
    recommendationId: string,
    category: string,
    count: number = 1,
    token?: string
) {
    const authToken = token || DEV_TOKEN;

    const response = await fetch(`${API_BASE_URL}/v2/recommendations/${recommendationId}/add-on`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${authToken}`
        },
        body: JSON.stringify({
            category,
            count
        }),
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Failed to request add-on for category: ${category}`);
    }

    return response.json();
}

export async function getRecommendationsAsync(
    data: UserInputV2,
    token?: string
) {
    const authToken = token || DEV_TOKEN;
    const response = await fetch(`${API_BASE_URL}/v2/recommendations/async`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${authToken}`
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}: Failed to start async recommendation`);
    }

    return response.json();
}

export async function pollJobStatus(
    jobId: string,
    token?: string
) {
    const authToken = token || DEV_TOKEN;
    const response = await fetch(`${API_BASE_URL}/v2/recommendations/status/${jobId}`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${authToken}`
        },
    });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}: Failed to poll job status`);
    }

    return response.json();
}
