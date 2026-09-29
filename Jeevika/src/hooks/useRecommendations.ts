import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { mockApi } from '../services/mockApi';
import { useAppStore } from '../stores/useAppStore';
import { BeneficiaryProfile } from '../types';

export function useRecommendations() {
  const queryClient = useQueryClient();
  const { profile, setRecommendations, setProfile } = useAppStore();

  const recommendationsQuery = useQuery({
    queryKey: ['recommendations', profile?.id],
    queryFn: async () => {
      const data = profile
        ? await mockApi.generateRecommendations(profile)
        : await mockApi.fetchRecommendations();
      setRecommendations(data);
      return data;
    },
    staleTime: 1000 * 60 * 5, // 5 minutes
  });

  const generateProfileMutation = useMutation({
    mutationFn: (answers: Record<string, string>) =>
      mockApi.generateProfileFromInterview(answers),
    onSuccess: (newProfile: BeneficiaryProfile) => {
      setProfile(newProfile);
      queryClient.invalidateQueries({ queryKey: ['recommendations'] });
    },
  });

  return {
    recommendations: recommendationsQuery.data || [],
    isLoading: recommendationsQuery.isLoading,
    isError: recommendationsQuery.isError,
    error: recommendationsQuery.error,
    generateProfile: generateProfileMutation.mutateAsync,
    isGeneratingProfile: generateProfileMutation.isPending,
  };
}
