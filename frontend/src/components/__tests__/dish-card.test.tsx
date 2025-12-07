import { render, screen } from '@testing-library/react';
import { DishCard } from '../dish-card';
import type { MenuItem } from '@/types';

const mockDish: MenuItem = {
  dish_id: '1',
  dish_name: '小籠包',
  price: 200,
  reason: '經典必點，皮薄餡多',
  category: '點心',
  review_count: 1500,
  price_estimated: false,
  quantity: 1,
};

const defaultProps = {
  item: mockDish,
  status: 'pending' as const,
  onSelect: jest.fn(),
  onSwap: jest.fn(),
  isSwapping: false,
};

describe('DishCard Component', () => {
  it('renders dish information correctly', () => {
    render(<DishCard {...defaultProps} />);

    expect(screen.getByText('小籠包')).toBeInTheDocument();
    expect(screen.getByText('NT$ 200')).toBeInTheDocument();
    expect(screen.getByText('"經典必點，皮薄餡多"')).toBeInTheDocument();
    // Category is currently commented out in the component
    // expect(screen.getByText('點心')).toBeInTheDocument();
  });

  it('shows review count when available', () => {
    render(<DishCard {...defaultProps} />);
    expect(screen.getByText(/1500.*好評/)).toBeInTheDocument();
  });

  it('shows estimated price indicator', () => {
    const estimatedDish = { ...mockDish, price_estimated: true };
    render(<DishCard {...defaultProps} item={estimatedDish} />);
    expect(screen.getByText('估價')).toBeInTheDocument();
  });
});
